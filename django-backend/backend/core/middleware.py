from django.conf import settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    HASH_SESSION_KEY,
    SESSION_KEY,
    _get_user_session_key,
    constant_time_compare,
    get_backends,
    load_backend,
    login,
    logout,
)
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.utils.functional import SimpleLazyObject

from .backends import IAPBackend


def get_user_object(request):
    """
    Return the user model instance associated with the given request session.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    from django.contrib.auth.models import AnonymousUser

    user = None
    try:
        user_id = _get_user_session_key(request)
        backend_path = request.session[BACKEND_SESSION_KEY]
    except KeyError:
        pass
    else:
        if backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = load_backend(backend_path)
            user = backend.get_user(user_id)
            # Verify the session
            if hasattr(user, "get_session_auth_hash"):
                session_hash = request.session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash, user.get_session_auth_hash()
                )
                if not session_hash_verified:
                    request.session.flush()
                    user = None

    return user or AnonymousUser()


def get_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = get_user_object(request)
    return request._cached_user


class AuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        # assert hasattr(request, "session"), (
        #     "The djangae.contrib.googleauth middleware requires session middleware "
        #     "to be installed. Edit your MIDDLEWARE%s setting to insert "
        #     "'django.contrib.sessions.middleware.SessionMiddleware' before "
        #     "'djangae.contrib.googleauth.middleware.AuthenticationMiddleware'."
        # ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")

        request.user = SimpleLazyObject(lambda: get_user(request))

        # See if the handling view is marked with the auth_middleware_exempt
        # decorator, and return if so.
        if request.resolver_match:
            func = request.resolver_match.func
            exempt = getattr(func, "_auth_middleware_exempt", False)
            if exempt:
                return None

        backend_str = request.session.get(BACKEND_SESSION_KEY)

        if request.user.is_authenticated:
            if backend_str and isinstance(load_backend(backend_str), IAPBackend):
                if not IAPBackend.can_authenticate(request):
                    logout(request)
        else:
            backends = get_backends()
            try:
                iap_backend = next(
                    filter(lambda be: isinstance(be, IAPBackend), backends)
                )
            except StopIteration:
                iap_backend = None

            # Try to authenticate with IAP if the headers
            # are available
            if iap_backend and IAPBackend.can_authenticate(request):
                # Calling login() cycles the csrf token which causes POST request
                # to break. We only call login if authenticating with IAP changed
                # the user ID in the session, or the user ID was not in the session
                # at all.
                user = iap_backend.authenticate(request)
                if user and user.is_authenticated:
                    should_login = (
                        SESSION_KEY not in request.session
                        or _get_user_session_key(request) != user.pk
                    )

                    # We always set the backend to IAP so that it truely reflects what was the last
                    # backend to authenticate this user
                    user.backend = (
                        "djangae.contrib.googleauth.backends.iap.%s"
                        % IAPBackend.__name__
                    )

                    if should_login:
                        # Setting the backend is needed for the call to login
                        login(request, user)
                    else:
                        # If we don't call login, we need to set request.user ourselves
                        # and update the backend string in the session
                        request.user = user
                        request.session[BACKEND_SESSION_KEY] = user.backend
