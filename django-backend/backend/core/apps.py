from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from firebase_admin import credentials as firebase_credentials
from firebase_admin import initialize_app as initialize_firebase_app


def _check_task_environment_middleware():
    enabled = "backend.core.middleware.TaskEnvironmentMiddleware" in settings.MIDDLEWARE

    if not enabled:
        raise ImproperlyConfigured(
            "You must add backend.core.middleware.TaskEnvironmentMiddleware "
            "to your MIDDLEWARE setting to make use of the Cloud Tasks integration."
        )


def _patch_django_redirect_to_login():
    import django.contrib.auth.views
    from django.contrib.auth import REDIRECT_FIELD_NAME

    old_fn = django.contrib.auth.views.redirect_to_login
    resolved_login_url = reverse_lazy("core:gae_login_redirect")

    def _wrapper(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
        # Override the login_url to always use the GAE login_redirect
        return old_fn(
            next,
            login_url=resolved_login_url,
            redirect_field_name=redirect_field_name,
        )

    django.contrib.auth.views.redirect_to_login = _wrapper


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.core"

    def ready(self) -> None:
        _check_task_environment_middleware()

        # Patch Django Admin login redirect on remote environments
        if settings.REMOTE_ENVIRONMENT:
            _patch_django_redirect_to_login()

        firebase_cred = firebase_credentials.ApplicationDefault()
        # TODO: template here
        initialize_firebase_app(
            firebase_cred,
            {"projectId": "net-startupworx-bloxtest10"},
        )
        return super().ready()
