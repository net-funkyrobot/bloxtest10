from datetime import datetime
from typing import Optional

from django.db import transaction
from firebase_admin import firestore
from ninja import Schema

from backend.core.models import MobileAppUser
from backend.core.schema import FirestoreUserProfile
from backend.core.services.base import ServiceResult, catch_service_errors


class SyncNewUsers(Schema):
    """Sync user profile documents from Firestore.

    This creates user profiles in the backend database.
    """

    sync_all: bool = False
    sync_from: Optional[datetime]

    @catch_service_errors
    def run(self) -> ServiceResult[None]:
        last_sync_timestamp = self.sync_from or (
            MobileAppUser.objects.values_list("created_at", flat=True)
            .order_by("-created_at")
            .first()
        )

        store = firestore.client()

        if self.sync_all or last_sync_timestamp is None:
            fb_users = store.collection("users").get()
        else:
            fb_users = (
                store.collection("users")
                .where("created", ">=", last_sync_timestamp)
                .stream()
            )

        # Successfully sync all users or none at all
        # This is so we can retry whole syncs after fixing an error and no
        # user profiles fall down the cracks
        with transaction.atomic():
            for user in fb_users:
                user_profile = FirestoreUserProfile(**user.to_dict())

                MobileAppUser.objects.get_or_create(
                    uid=user.reference.id,
                    email=user_profile.email,
                )

        return ServiceResult(success=True)
