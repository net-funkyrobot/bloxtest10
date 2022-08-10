from functools import partial

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.utils import timezone

from backend.core.models import GaeAbstractBaseUser


class AppEngineUserAPIBackend(ModelBackend):
    atomic = partial(transaction.atomic)
    atomic_kwargs = {}

    def authenticate(self, request, **kwargs):
        """Handle authentication of a user from the given credentials.

        Credentials must be a 'google_user' as returned by the App Engine
        Users API.
        """  # noqa: DAR401
        google_user = kwargs.get("google_user", None)

        if google_user is None:
            return None

        User = get_user_model()  # noqa: N806

        if not issubclass(User, GaeAbstractBaseUser):
            raise ImproperlyConfigured(
                "AppEngineUserAPIBackend requires AUTH_USER_MODEL to be a "
                " subclass of djangae.contrib.auth.base.GaeAbstractBaseUser."
            )

        user_id = google_user.user_id()
        email = BaseUserManager.normalize_email(
            google_user.email()
        )  # Normalizes the domain only.

        try:
            # User exists and we can bail immediately
            user = User.objects.get(google_user_id=user_id)
            return user
        except User.DoesNotExist:
            pass

        try:
            # Users that existed before the introduction of the `email_lower`
            # field will not have that field, but will most likely have a lower
            # case email address because we used to lower case the email field
            existing_user = User.objects.get(email_lower=email.lower())
        except User.DoesNotExist:
            # User doesn't exist, is not an admin and we aren't going to
            # create one.
            return None

        # OK. We will grant access. We may need to update an existing user, or
        # create a new one, or both.
        #
        # Those 2 scenarios are:
        # 1. A User object has been created for this user, but that they have
        # not logged in yet using their Google account. In this case we fetch
        # the User object by email, and then update it with the Google User ID.
        #
        # 2. A User object exists for this email address but belonging to a
        # different Google account. This generally only happens when the email
        # address of a Google Apps account has been signed up as a Google
        # account and then the apps account itself has actually become a Google
        # account. This is possible but very unlikely.

        if existing_user:
            # We can use the existing user for this new login.
            existing_user.google_user_id = user_id
            existing_user.last_login = timezone.now()
            existing_user.save()

            return existing_user
