from django.db import models

from .base import FIRESTORE_STRING_MAX_LENGTH, TimestampsMixin


class MobileAppUser(TimestampsMixin):
    uid = models.CharField(
        max_length=FIRESTORE_STRING_MAX_LENGTH,
        unique=True,
        help_text="Firebase Auth User ID",
    )
    email = models.EmailField(db_index=True)
    subscribed = models.BooleanField(
        default=False,
        help_text="Marks if the user has been subscribed to the mailing list",
    )
    has_unsubscribed = models.BooleanField(
        default=False,
        help_text="Marks if the user has unsubscribed themselves to the mailing "
        "list (we shouldn't subsequently re-add them).",
    )
    mailing_list_id = models.CharField(max_length=30, blank=True, null=True)
