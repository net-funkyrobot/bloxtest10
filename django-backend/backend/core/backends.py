from functools import partial

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from google.appengine.api import users

from backend.core.models import GaeAbstractBaseUser


class BaseAppEngineUserAPIBackend(ModelBackend):
    atomic = partial(transaction.atomic)
    atomic_kwargs = {}

    def authenticate(self, google_user=None):
        """Handle authentication of a user from the given credentials.

        Credentials must be a 'google_user' as returned by the App Engine
        Users API.
        """  # noqa: DAR401
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
            user = User.objects.get(username=user_id)
            return user
        except User.DoesNotExist:
            pass

        user_is_admin = users.is_current_user_admin()

        try:
            # Users that existed before the introduction of the `email_lower`
            # field will not have that field, but will most likely have a lower
            # case email address because we used to lower case the email field
            existing_user = User.objects.get(email_lower=email.lower())
        except User.DoesNotExist:
            if not user_is_admin:
                # User doesn't exist, is not an admin and we aren't going to
                # create one.
                return None

            existing_user = None

        # OK. We will grant access. We may need to update an existing user, or
        # create a new one, or both.
        #
        # Those 3 scenarios are:
        # 1. A User object has been created for this user, but that they have
        # not logged in yet. In this case we fetch the User object by email,
        # and then update it with the Google User ID.
        #
        # 2. A User object exists for this email address but belonging to a
        # different Google account. This generally only happens when the email
        # address of a Google Apps account has been signed up as a Google
        # account and then the apps account itself has actually become a Google
        # account. This is possible but very unlikely.
        #
        # 3. There is no User object relating to this user whatsoever.

        if existing_user:
            if existing_user.username is None:
                # We can use the existing user for this new login.
                existing_user.username = user_id
                existing_user.email = email
                existing_user.last_login = timezone.now()
                existing_user.save()

                return existing_user
            else:
                # We need to update the existing user and create a new one.
                with self.atomic(**self.atomic_kwargs):
                    existing_user = User.objects.get(pk=existing_user.pk)
                    existing_user.email = ""
                    existing_user.save()

                    return User.objects.create_user(user_id, email=email)
        else:
            # Create a new user, but account for another thread having created
            # it already in a race condition scenario.
            # Our logic cannot be in a transaction, so we have to just catch
            # this.
            try:
                return User.objects.create_user(user_id, email=email)
            except IntegrityError:
                return User.objects.get(username=user_id)
