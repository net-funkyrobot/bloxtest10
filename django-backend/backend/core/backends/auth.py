from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.db.models import Q
from django.db.transaction import atomic
from google.auth.transport import requests
from google.oauth2 import id_token
from structlog.stdlib import get_logger

from ..models.auth import AbstractIapAdminUser, UserManager

_GOOG_AUTHENTICATED_USER_ID_HEADER = "HTTP_X_GOOG_AUTHENTICATED_USER_ID"
_GOOG_AUTHENTICATED_USER_EMAIL_HEADER = "HTTP_X_GOOG_AUTHENTICATED_USER_EMAIL"
_GOOG_JWT_ASSERTION_HEADER = "HTTP_X_GOOG_IAP_JWT_ASSERTION"
_IAP_AUDIENCE = "/projects/440894321495/apps/net-startupworx-bloxtest10"

User = get_user_model()

if not issubclass(User, AbstractIapAdminUser):
    raise ImproperlyConfigured(
        "IAPAdminBackend requires AUTH_USER_MODEL to be a "
        " subclass of backend.core.models.auth.AbstractIapAdminUser."
    )

_logger = get_logger(__name__)


class IapAdminBackend(ModelBackend):
    @classmethod
    def can_authenticate(cls, request):
        return (
            _GOOG_AUTHENTICATED_USER_EMAIL_HEADER in request.META
            and _GOOG_AUTHENTICATED_USER_EMAIL_HEADER in request.META
            and _GOOG_JWT_ASSERTION_HEADER in request.META
        )

    def authenticate(self, request, **kwargs):
        error_partial = "An attacker might have tried to bypass IAP"
        user_id = request.META.get(_GOOG_AUTHENTICATED_USER_ID_HEADER)
        email = request.META.get(_GOOG_AUTHENTICATED_USER_EMAIL_HEADER)

        # User not logged in to IAP
        if not user_id or not email:
            return

        # All IDs provided should be namespaced
        if ":" not in user_id or ":" not in email:
            return

        # Google tokens are namespaced with "auth.google.com:"
        namespace, user_id = user_id.split(":", 1)
        _, email = email.split(":", 1)

        audience = _IAP_AUDIENCE
        iap_jwt = request.META.get(_GOOG_JWT_ASSERTION_HEADER)

        try:
            signed_user_id, signed_user_email = _validate_iap_jwt(iap_jwt, audience)
            signed_user_namespace, signed_user_id = signed_user_id.split(":", 1)
        except ValueError as e:
            raise SuspiciousOperation(
                "**ERROR: JWT validation error {}**\n{}".format(e, error_partial)
            )

        assert signed_user_id == user_id, (
            f"IAP signed user id does not match {0}. {1}.".format(
                _GOOG_AUTHENTICATED_USER_ID_HEADER,
                error_partial,
            ),
        )
        assert signed_user_email == email, (
            f"IAP signed user email does not match {0}. {1}.".format(
                _GOOG_AUTHENTICATED_USER_EMAIL_HEADER,
                error_partial,
            ),
        )

        email = UserManager.normalize_email(email)
        assert email

        with atomic():
            # Look for a user, either by ID, or email
            user = User.objects.filter(google_iap_id=user_id).first()
            if not user:
                # We explicitly don't do an OR query here, because we only want
                # to search by email if the user doesn't exist by ID. ID takes
                # precendence.
                user = User.objects.filter(
                    Q(email_lower=email.lower()) | Q(email=email)
                ).first()

                if user and user.google_iap_id:
                    _logger.warning(
                        "Found an existing user by email ({0}) who had a different "
                        "IAP user ID ({1} != {2}). This seems like a bug.".format(
                            email,
                            user.google_iap_id,
                            user_id,
                        )
                    )

                    # We don't use this to avoid accidentally "stealing" another
                    # user
                    user = None

            if user:
                # So we previously had a user sign in by email, but not
                # via IAP, so we should set that ID
                if not user.google_iap_id:
                    user.google_iap_id = user_id
                    user.google_iap_namespace = namespace
                else:
                    # Should be caught above if this isn't the case
                    assert user.google_iap_id == user_id

                # Update the email as it might have changed or perhaps
                # this user was added through some other means and the
                # sensitivity of the email differs etc.
                user.email = email

                # If the user doesn't currently have a password, it could
                # mean that this backend has just been enabled on existing
                # data that uses some other authentication system (e.g. the
                # App Engine Users API) - for safety we make sure that an
                # unusable password is set.
                if not user.password:
                    user.set_unusable_password()

                # Note we don't update the username, as that may have
                # been overridden by something post-creation
                user.save()
            else:
                with atomic():
                    # First time we've seen this user
                    user = User.objects.create(
                        google_iap_id=user_id,
                        google_iap_namespace=namespace,
                        email=email,
                        # We create users as admins because IAP users will be
                        # Google Workspace users internal to our organisation
                        is_staff=True,
                    )
                    user.set_unusable_password()
                    user.save()

        return user


def _validate_iap_jwt(iap_jwt, expected_audience):
    """Validate an IAP JWT.

    Args:
      iap_jwt: The contents of the X-Goog-IAP-JWT-Assertion header.
      expected_audience: The Signed Header JWT audience. See
          https://cloud.google.com/iap/docs/signed-headers-howto
          for details on how to get this value.

    Returns:
      (user_id, user_email).
    """

    decoded_jwt = id_token.verify_token(
        iap_jwt,
        requests.Request(),
        audience=expected_audience,
        certs_url="https://www.gstatic.com/iap/verify/public_key",
    )
    return (decoded_jwt["sub"], decoded_jwt["email"])
