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
