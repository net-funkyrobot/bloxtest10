from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    authenticate,
    get_user,
    load_backend,
    login,
    logout,
)
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.models import AnonymousUser, BaseUserManager
from google.appengine.api import users

from backend.core.backends import AppEngineUserAPIBackend


class GaeAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        django_user = get_user(request)
        google_user = users.get_current_user()

        # Check to see if the user is authenticated with a different backend,
        # if so, just set request.user and bail
        if django_user.is_authenticated:
            backend_str = request.session.get(BACKEND_SESSION_KEY)
            if (not backend_str) or not isinstance(
                load_backend(backend_str), AppEngineUserAPIBackend
            ):
                request.user = django_user
                return

        if django_user.is_anonymous and google_user:
            # If there is a google user, but we are anonymous, log in!
            # Note that a Django user must already exist or have been
            # pre-created for this google user.
            django_user = (
                authenticate(request, google_user=google_user) or AnonymousUser()
            )
            if django_user.is_authenticated:
                login(request, django_user)

        if django_user.is_authenticated:
            if not google_user:
                # If we are logged in with django, but no longer logged in
                # with Google then log out
                logout(request)
                django_user = AnonymousUser()
            elif django_user.google_user_id != google_user.user_id():
                # If the Google user changed, we need to log in with the new one
                logout(request)
                django_user = authenticate(google_user=google_user) or AnonymousUser()
                if django_user.is_authenticated:
                    login(request, django_user)

        # Note that the logic above may have logged us out, hence new `if` statement
        if django_user.is_authenticated:
            self.sync_user_data(django_user, google_user)

        request.user = django_user

    def sync_user_data(self, django_user, google_user):
        # Now make sure we update is_superuser and is_staff appropriately
        changed_fields = []

        is_superuser = users.is_current_user_admin()

        if is_superuser != django_user.is_superuser:
            django_user.is_superuser = django_user.is_staff = is_superuser
            changed_fields += ["is_superuser", "is_staff"]

        email = BaseUserManager.normalize_email(
            google_user.email()
        )  # Normalizes the domain only.

        if email != django_user.email:
            django_user.email = email
            changed_fields += ["email", "email_lower"]

        if changed_fields:
            django_user.save(update_fields=changed_fields)
