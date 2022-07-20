# flake8: noqa

import os

from backend.settings import (
    ALLOWED_HOSTS,
    AUTH_PASSWORD_VALIDATORS,
    BASE_DIR,
    DEFAULT_AUTO_FIELD,
    INSTALLED_APPS,
    MIDDLEWARE,
    LANGUAGE_CODE,
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
