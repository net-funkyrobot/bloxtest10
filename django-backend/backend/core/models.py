from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

from backend.core.fields import (
    AutoCreatedField,
    AutoUpdatedField,
    CharOrNoneField,
    ComputedCharField,
)
from backend.core.utils import validate_google_user_id

FIRESTORE_STRING_MAX_LENGTH = 128


class TimestampsMixin(models.Model):
    created_at = AutoCreatedField()
    updated_at = AutoUpdatedField()

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


class GaeUserManager(UserManager):
    def pre_create_google_user(self, email, **extra_fields):
        """Pre-create a User object for a user logging in later via Google Accounts."""
        values = {
            "is_active": True,  # defaults which can be overridden
        }
        values.update(**extra_fields)
        values.update(
            # things which cannot be overridden
            email=self.normalize_email(email),  # lowercase the domain only
            username=None,
            password=make_password(None),  # unusable password
            # Stupidly, last_login is not nullable, so we can't set it to None.
        )
        return self.create(**values)


def _get_email_lower(user):
    """Compute lowercase email field."""
    # Note that the `email` field is not nullable, but the `email_lower` one is
    # nullable and must not contain empty strings because it is unique
    return user.email and user.email.lower() or None


class GaeAbstractBaseUser(AbstractBaseUser):
    """Absract base class for creating a User model which works with the App
    Engine users API.
    """  # noqa: D205, D400

    username = CharOrNoneField(
        # This stores the Google user_id, or custom username for
        # non-Google-based users. We allow it to be null so that Google-based
        # users can be pre-created before they log in.
        _("User ID"),
        max_length=21,
        unique=True,
        blank=True,
        null=True,
        default=None,
        validators=[validate_google_user_id],
    )
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)

    # Email addresses are case sensitive, but many email systems and many people
    # treat them as if they're not.  We must store the case-preserved email
    # address to ensure that sending emails always works, but we must be able
    # to query for them case insensitively and therefore we must enforce
    # uniqueness on a case insensitive basis, hence these 2 fields
    email = models.EmailField(_("email address"))
    # The null-able-ness of the email_lower is only to deal with when an email
    # address moves between Google Accounts and therefore we need to wipe it
    # without breaking the unique constraint.
    email_lower = ComputedCharField(
        _get_email_lower, max_length=email.max_length, unique=True, null=True
    )

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

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = GaeUserManager()

    class Meta:
        abstract = True

    def clean(self):
        # Only call up if username is not none. Parent's clean() stringifies
        # username blindly
        if self.get_username() is not None:
            super(GaeAbstractBaseUser, self).clean()

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """Return first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """Send an email to this User."""
        # TODO: Configure email through legacy mail API?
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        """Override this as username is nullable.

        We either return the email address, or if there is a username, we
        return "email (username)".
        """
        username = self.get_username()
        if username:
            return "{0} ({1})".format(self.email, username)
        return self.email

    def validate_unique(self, exclude=None):
        """Check email address does not already exist.

        Queries on on email_lower.
        """  # noqa: DAR401
        exclude = exclude or []
        if "email_lower" not in exclude:
            # We do our own check using the email_lower field, so we don't need
            # Django to query on it as well
            exclude.append("email_lower")

        try:
            super(GaeAbstractBaseUser, self).validate_unique(exclude=exclude)
        except ValidationError as super_error:  # noqa: F841
            pass
        else:
            super_error = None

        if self.email and "email" not in exclude:
            existing = self.__class__.objects.filter(email_lower=self.email.lower())
            if not self._state.adding:
                existing = existing.exclude(pk=self.pk)
            if existing.exists():
                model_name = self._meta.verbose_name
                field_name = self._meta.get_field("email").verbose_name
                message = "%s with this %s already exists" % (model_name, field_name)
                error_dict = {"email": [message]}
                if super_error:
                    super_error.update_error_dict(error_dict)
                    raise super_error
                else:
                    raise ValidationError(error_dict)
        elif super_error:
            raise


class GaeUser(GaeAbstractBaseUser, PermissionsMixin):
    """A basic user model which can be used with GAE authentication.

    Essentially the equivalent of django.contrib.auth.models.User.
    """

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("user")
        verbose_name_plural = _("users")
