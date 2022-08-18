import functools
import os
import pickle
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional
from urllib.parse import unquote

import grpc
import structlog
from django.conf import settings
from django.db import connections
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_str
from google.api_core import exceptions
from google.cloud import tasks_v2
from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel, conint, validator

from .environment import gae_version, tasks_location
from .models import LargeDeferredTask

logger = structlog.get_logger(__name__)

_DEFAULT_QUEUE = "default"
_DEFAULT_URL = reverse_lazy("tasks_deferred_handler")
_TASKQUEUE_HEADERS = {"Content-Type": "application/octet-stream"}
_CLOUD_TASKS_PROJECT = settings.GOOGLE_CLOUD_PROJECT
_CLOUD_TASKS_LOCATION = tasks_location()


def get_cloud_tasks_client():
    """Get an instance of a Google CloudTasksClient."""

    if settings.REMOTE_ENVIRONMENT:
        return tasks_v2.CloudTasksClient()
    else:
        # Running locally, try to connect to the emulator
        from google.api_core.client_options import ClientOptions
        from google.cloud.tasks_v2.services.cloud_tasks.transports.grpc import (
            CloudTasksGrpcTransport,
        )

        host = os.environ.get("TASKS_EMULATOR_HOST", "127.0.0.1:9022")

        client = tasks_v2.CloudTasksClient(
            transport=CloudTasksGrpcTransport(channel=grpc.insecure_channel(host)),
            client_options=ClientOptions(api_endpoint=host),
        )
        return client


def cloud_tasks_parent_path():
    location_id = _CLOUD_TASKS_LOCATION
    project_id = _CLOUD_TASKS_PROJECT

    assert project_id
    assert location_id

    return "projects/{0}/locations/{1}".format(project_id, location_id)


def cloud_tasks_queue_path(queue_name):
    """Return the full path to a Cloud Tasks queue."""
    return "{0}/queues/{1}".format(cloud_tasks_parent_path(), queue_name)


class TaskError(Exception):
    """Base class for exceptions in this module."""


class PermanentTaskError(TaskError):
    """Indicates that a task failed, and will never succeed."""


class SingularTaskError(TaskError):
    """Indicates that a task failed once."""


class RoutingOptions(BaseModel):
    version: str = gae_version()
    serivce: Optional[str]
    instance: Optional[str]


class TaskOptions(BaseModel):
    name: Optional[str]
    created_at: Optional[datetime]
    small_task: bool = False
    using: str = "default"
    transactional: bool = False  # TODO: Should this be False by default?
    countdown: Optional[conint(gt=0)]
    eta: Optional[datetime]
    routing: RoutingOptions = RoutingOptions()
    handler_url: str = unquote(force_str(_DEFAULT_URL))
    extra_task_headers: dict = {}
    queue: str = _DEFAULT_QUEUE

    @validator("using")
    def using_has_valid_connection_name(cls, v):
        if v not in connections:
            raise ValueError(
                "'using' not a valid DB connection in {0}".format(
                    ",".join(connections.keys()),
                )
            )

        return v


def _run_from_database(deferred_task_id):
    """Retrieve a task from the database and execute it."""

    def run(data):
        # Unpickle and execute task.
        try:
            service_instance = pickle.loads(data)
        except Exception as e:
            raise PermanentTaskError(e)
        else:
            return service_instance.run()

    entity = LargeDeferredTask.objects.filter(pk=deferred_task_id).first()
    if not entity:
        raise PermanentTaskError()

    try:
        run(entity.data)
        entity.delete()
    except PermanentTaskError:
        entity.delete()
        raise


def _serialize(obj: object):
    return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)


def _get_task_name(obj: Any, task_created_at: datetime) -> str:
    klass = obj.__class__
    task_id = str(uuid.uuid4())[:8]
    if klass.__module__:
        name = "{0}.{1}:{2}-{3}".format(
            klass.__module__,
            klass.__qualname__,
            task_created_at,
            task_id,
        )
    else:
        name = "{0}:{1}-{2}".format(klass.__qualname__, task_created_at, task_id)

    return name


def _schedule_task(pickled_data: bytes, task_options: TaskOptions):
    client = get_cloud_tasks_client()
    deferred_task = None

    # Use a db entity unless this has been explicitly marked as a small task
    if not task_options.small_task:
        deferred_task = LargeDeferredTask.objects.create(data=pickled_data)

    path = client.queue_path(
        _CLOUD_TASKS_PROJECT,
        _CLOUD_TASKS_PROJECT,
        task_options.queue,
    )

    task_headers = dict(_TASKQUEUE_HEADERS)
    task_headers.update(task_options.extra_task_headers)

    schedule_time = task_options.eta
    if task_options.countdown:
        schedule_time = timezone.now() + timedelta(seconds=task_options.countdown)

    if schedule_time:
        # If a schedule time has bee requested, we need to convert
        # to a Timestamp
        ts = Timestamp()
        ts.FromDatetime(schedule_time)
        schedule_time = ts

    created_at_ts = Timestamp()
    created_at_ts.FromDatetime(task_options.created_at)

    task = {
        "name": task_options.name,
        "create_time": created_at_ts,
        "schedule_time": schedule_time,
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": "POST",
            "relative_uri": task_options.handler_url,
            "body": pickled_data,
            "headers": task_headers,
            "app_engine_routing": task_options.routing,
        },
    }

    try:
        # Defer the task
        task = client.create_task(parent=path, task=task)  # FIXME: Handle transactional

        # Delete the key as it wasn't needed
        if deferred_task:
            deferred_task.delete()
    except exceptions.InvalidArgument as e:
        if "Task size too large" not in str(e):
            raise

        # Create a db entity unless this has been explicitly marked as a small task
        if task_options.small_task:
            raise
        deferred_task = LargeDeferredTask.objects.create(data=pickled_data)

        # Replace the task body with one containing a function to run the
        # original task body which is stored in the datastore entity.
        task["body"] = _serialize(_run_from_database, deferred_task.pk)

        client.create_task(path, task)  # FIXME: Handle transactional
    except:  # noqa
        # Any other exception? Delete the key
        if deferred_task:
            deferred_task.delete()
        raise


def defer(obj: object, task_options: Optional[TaskOptions] = None):
    """
    This is a reimplementation of the defer() function that historically shipped
    with App Engine Standard before the Python 3 runtime.

    It fixes a number of bugs in that implementation, but has some subtle
    differences. In particular, the _transactional flag is not entirely atomic
    - deferred tasks will run on successful commit, but they're not *guaranteed*
    to run if there is an error submitting them.

    If the task is too large to be serialized and passed in the request it uses
    a Django model instance to tempoarilly store the payload. The small task
    limit is 100K.
    """
    assert callable(getattr(obj, "run")), "Task 'obj' must have a run() method."

    task_options = task_options.copy() if task_options else TaskOptions()

    # Populate task name unless custom name given
    created_at = datetime.now()
    task_options.created_at = task_options.created_at or created_at
    task_options.name = task_options.name or _get_task_name(
        obj,
        task_options.created_at,
    )

    # Determine if we run the task at the end of the current transaction
    connection = connections[task_options.using]
    task_options.transactional = (
        task_options.transactional
        if task_options.transactional is not None
        else connection.in_atomic_block
    )

    pickled = _serialize(obj)

    if task_options.transactional:
        # Django connections have an on_commit message that run things on
        # post-commit.
        connection.on_commit(functools.partial(_schedule_task, pickled, task_options))
    else:
        _schedule_task(pickled, task_options)
