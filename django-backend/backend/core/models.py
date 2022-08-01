import re

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

FIRESTORE_STRING_MAX_LENGTH = 128


class TimestampsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


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


def _validate_google_user_id(value):
    """Validate the given value is either empty, None, or 21 digits.

    Raises:
        ValidationError: if Google user ID is invalid.
    """
    if value and not re.match(r"^\d{21}$", value):
        raise ValidationError("Google user ID should be 21 digits.")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password."""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class GaeAbstractBaseUser(AbstractBaseUser):
    """Abstract model which works with the AppEngine users API."""

    email = models.EmailField(_("email address"), unique=True)

    google_user_id = models.CharField(
        # This stores the AppEngine Users API user ID. We allow it to be null
        # so that Google-based users can be pre-created before they log in and
        # they can use passwords locally.
        _("Google user ID"),
        max_length=21,
        unique=True,
        default=None,
        null=True,
        blank=True,
        validators=[_validate_google_user_id],
    )

    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    email_lower = models.EmailField(unique=True, editable=False)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def get_full_name(self):
        """Return first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def save(self, *args, **kwargs):
        self.email_lower = self.email.lower()
        super().save(*args, **kwargs)


class BackendUser(GaeAbstractBaseUser, PermissionsMixin):
    pass
