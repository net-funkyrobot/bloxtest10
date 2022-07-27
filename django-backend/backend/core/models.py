from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from backend.core.fields import AutoCreatedField, AutoUpdatedField

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


class AbstractBackendUser(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    google_iap_id = models.CharField(
        max_length=150,
        unique=True,
        default=None,
        null=True,
        blank=True,
    )

    google_iap_namespace = models.CharField(
        max_length=64,
        default="",
        blank=True,
    )

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # Lower-cased versions of fields for querying on Cloud Datastore
    username_lower = models.CharField(max_length=150, unique=True, editable=False)
    email_lower = models.EmailField(unique=True, editable=False)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        from django.contrib.auth.models import _user_has_perm

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        from django.contrib.auth.models import _user_has_module_perms

        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username_lower = self.username.lower()
        self.email_lower = self.email.lower()
        super().save(*args, **kwargs)


class BackendUser(AbstractBackendUser, PermissionsMixin):
    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("user")
        verbose_name_plural = _("users")
