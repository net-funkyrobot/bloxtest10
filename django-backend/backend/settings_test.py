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
)

# Use a local SQLlite database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db_test.sqlite3"),
    }
}
