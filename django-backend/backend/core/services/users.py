from datetime import datetime
from typing import Optional

from firebase_admin import firestore
from ninja import Schema
from pydantic import ValidationError

from backend.core.models import UserProfile
from backend.core.schema import FirestoreUserProfile, ServiceResult


class SyncNewUsers(Schema):
    """
    Sync user profile documents from Firestore and create user profiles in the
    backend database.
    """

    sync_all: bool = False
    sync_from: Optional[datetime]

    def run(self) -> ServiceResult[None]:
        last_sync_timestamp = self.sync_from or (
            UserProfile.objects.values_list("created_at", flat=True)
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

        for user in fb_users:
            try:
                user_profile = FirestoreUserProfile(**user.to_dict())
            except ValidationError:
                # TODO: log this out here
                continue

            obj, created = UserProfile.objects.get_or_create(
                firebase_auth_user_id=user.reference.id,
                email=user_profile.email,
            )

        return ServiceResult(success=True)
