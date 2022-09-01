from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from firebase_admin import credentials as firebase_credentials
from firebase_admin import initialize_app as initialize_firebase_app


def _check_task_environment_middleware():
    enabled = "backend.core.middleware.TaskEnvironmentMiddleware" in settings.MIDDLEWARE

    if not enabled:
        raise ImproperlyConfigured(
            "You must add backend.core.middleware.TaskEnvironmentMiddleware "
            "to your MIDDLEWARE setting to make use of the Cloud Tasks integration."
        )


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.core"

    def ready(self) -> None:
        _check_task_environment_middleware()

        firebase_cred = firebase_credentials.ApplicationDefault()
        # TODO: template here
        initialize_firebase_app(
            firebase_cred,
            {"projectId": "net-startupworx-bloxtest10"},
        )
        return super().ready()
