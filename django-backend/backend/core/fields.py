from django.core.exceptions import ImproperlyConfigured
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


class CharOrNoneField(models.CharField):
    """Store only non-empty strings or None (it won't store empty strings).

    This is useful if you want values to be unique but also want to allow empty values.
    """

    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        # Don't allow null=False because that would be insane.
        if not kwargs.get("null", True):
            raise ImproperlyConfigured("You can't set null=False on a CharOrNoneField.")
        # Set blank=True as the default, but allow it to be overridden, as it's
        # theoretically possible that you might want to prevent emptiness only
        # in a form
        defaults = dict(null=True, blank=True, default=None)
        defaults.update(**kwargs)
        super(CharOrNoneField, self).__init__(*args, **defaults)

    def pre_save(self, model_instance, add):
        value = super(CharOrNoneField, self).pre_save(model_instance, add)
        # Change empty strings to None
        if not value:
            return None
        return value


class ComputedFieldMixin:
    def __init__(self, func, *args, **kwargs):
        self.computer = func

        kwargs["editable"] = False

        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = self.get_computed_value(model_instance)
        setattr(model_instance, self.attname, value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        args = [self.computer] + args
        del kwargs["editable"]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, **kwargs):
        if value is None:
            return value
        return self.to_python(value)

    def get_computed_value(self, model_instance):
        # self.computer is either a function or a string containing the name of a method
        if callable(self.computer):
            return self.computer(model_instance)
        else:
            computer = getattr(model_instance, self.computer)
            return computer()


class ComputedCharField(ComputedFieldMixin, models.CharField):
    pass


class ComputedIntegerField(ComputedFieldMixin, models.IntegerField):
    pass


class ComputedTextField(ComputedFieldMixin, models.TextField):
    pass


class ComputedPositiveIntegerField(ComputedFieldMixin, models.PositiveIntegerField):
    pass


class ComputedBooleanField(ComputedFieldMixin, models.BooleanField):
    pass


class ComputedNullBooleanField(ComputedFieldMixin, models.NullBooleanField):
    pass
