from django.db import models

FIRESTORE_STRING_MAX_LENGTH = 128


class TimestampsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
