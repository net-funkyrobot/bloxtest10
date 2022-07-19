from django.db import models
from django.utils import timezone

FIRESTORE_STRING_MAX_LENGTH = 128


class AutoCreatedField(models.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("default", timezone.now)
        super().__init__(*args, **kwargs)


class AutoUpdatedField(AutoCreatedField):
    def pre_save(self, model_instance, add):
        now = timezone.now()
        setattr(model_instance, self.attname, now)
        return now


class TimestampsMixin(models.Model):
    created_at = AutoCreatedField()
    updated_at = AutoUpdatedField()

    class Meta:
        abstract = True


class UserProfile(TimestampsMixin):
    firebase_auth_user_id = models.CharField(
        max_length=FIRESTORE_STRING_MAX_LENGTH,
        unique=True,
    )
    email = models.EmailField()
    subscribed_to_mailing_list = models.BooleanField(default=False)
    has_unsubscribed = models.BooleanField(default=False)
