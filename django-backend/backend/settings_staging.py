# flake8: noqa

import os

from backend.settings import (
    ALLOWED_HOSTS,
    AUTH_PASSWORD_VALIDATORS,
    AUTH_USER_MODEL,
    AUTHENTICATION_BACKENDS,
    BASE_DIR,
    DEBUG,
    DEFAULT_AUTO_FIELD,
    INSTALLED_APPS,
    MAILERLITE_API_TOKEN,
    MIDDLEWARE,
    LANGUAGE_CODE,
    LOGGING,
    ROOT_URLCONF,
    SECRET_KEY,
    STATIC_ROOT,
    STATIC_URL,
    STATICFILES_DIRS,
    TEMPLATES,
    TIME_ZONE,
    USE_I18N,
    USE_L10N,
    USE_TZ,
    WSGI_APPLICATION,
    get_secrets,
)

# Load secrets via django-environ
env = get_secrets()

# Database
# Use django-environ to parse the connection string
DATABASES = {"default": env.db()}  # noqa: WPS407

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432

# Integrations

# Set MAILERLITE_GROUP to "testing" so test contacts don't pollute the mailing list
MAILERLITE_GROUP = "testing"
