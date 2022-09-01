from django.contrib.auth import BACKEND_SESSION_KEY, authenticate, load_backend, login
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser

from backend.core.backends import IapAdminBackend


def _iap_admin_authentication_middleware(get_response):
    def middleware(request):
        assert hasattr(request, "session"), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'backend.core.middleware.IapAdminAuthenticationMiddleware'."
        )

        user = get_user(request)

        # Check to see if the user is authenticated with a different backend,
        # if so, just set request.user and bail
        if user.is_authenticated:
            backend_str = request.session.get(BACKEND_SESSION_KEY)
            if (not backend_str) or not isinstance(
                load_backend(backend_str), IapAdminBackend
            ):
                request.user = user
                return

        # If we can authenticate, but we are anonymous, log in!
        if user.is_anonymous and IapAdminBackend.can_authenticate(request):
            user = authenticate(request) or AnonymousUser()
            if user.is_authenticated:
                login(request, user)

        request.user = user

        return get_response(request)

    return middleware


IapAdminAuthenticationMiddleware = _iap_admin_authentication_middleware
