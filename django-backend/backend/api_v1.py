from logging import getLogger

from ninja import NinjaAPI, Schema
from ninja.responses import Response
from structlog.stdlib import get_logger

from backend.core.tasks import defer

api = NinjaAPI()

_logger = get_logger(__name__)
_core_logger = getLogger(__name__)


class DummyBackgroundTask(Schema):
    some_param: int

    def run(self):
        _logger.error("Hello world! {0}".format(self.some_param))
        _core_logger.error("FUCK THIS")


@api.post("/dummy-resource")
def resource_with_background_task(request):
    defer(DummyBackgroundTask(some_param=1))


def openapi_yaml(request):
    breakpoint()
    schema = api.get_openapi_schema()
    return Response(schema)
