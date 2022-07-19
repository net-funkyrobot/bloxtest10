from django.apps import AppConfig
from firebase_admin import credentials as firebase_credentials
from firebase_admin import initialize_app as initialize_firebase_app


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.core"

    def ready(self) -> None:
        firebase_cred = firebase_credentials.ApplicationDefault()
        # TODO: template here
        initialize_firebase_app(
            firebase_cred,
            {"projectId": "net-startupworx-bloxtest10"},
        )
        return super().ready()
