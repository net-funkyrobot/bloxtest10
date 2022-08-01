import io
import os
from urllib.parse import urlparse

import environ
from google.cloud import secretmanager

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# On AppEngine this env variable should be set, locally this should be set in .envrc
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", None)
if not GOOGLE_CLOUD_PROJECT:
    raise Exception("No GOOGLE_CLOUD_PROJECT env var detected. Cannot continue.")


def is_remote_environment() -> bool:
    return "GAE_ENV" in os.environ


def get_secrets() -> environ.Env:
    """Get codebase secrets.

    Reads a local .secrets file OR loads secrets from GCloud Secret Manager.

    Raises:
        Exception: If no local .secrets file can be found and we're missing
            GOOGLE_CLOUD_PROJECT env variable to pull from Secret Manager.

    Returns:
        _type_: A Django-environ Env object.
    """
    env = environ.Env()
    env_file = os.path.join(BASE_DIR, ".secrets")

    if os.path.isfile(env_file):
        # Use a local secret file, if provided
        env.read_env(env_file)

    elif GOOGLE_CLOUD_PROJECT:
        # Pull secrets from Secret Manager
        project_id = GOOGLE_CLOUD_PROJECT

        client = secretmanager.SecretManagerServiceClient()
        settings_name = os.environ.get("SETTINGS_NAME", "backend_settings")
        name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
        env.read_env(io.StringIO(payload))

    else:
        raise Exception(
            "No local .secrets or GOOGLE_CLOUD_PROJECT detected. No secrets found."
        )

    return env


env = get_secrets()

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# Change this to 'False' when you are ready for production
DEBUG = False

# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to App Engine. This code takes the URL and converts it to both these settings formats.
APPENGINE_URL = env("APPENGINE_URL", default=None)
if APPENGINE_URL:
    # Ensure a scheme is present in the URL before it's processed.
    if not urlparse(APPENGINE_URL).scheme:
        APPENGINE_URL = f"https://{APPENGINE_URL}"

    ALLOWED_HOSTS = [urlparse(APPENGINE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [APPENGINE_URL]
    SECURE_SSL_REDIRECT = True
else:
    ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "backend.core",
]

MIDDLEWARE = [
    "django_structlog.middlewares.RequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# If we're connecting to production locally use the Django auth middleware,
# otherwise use GaeAuthenticationMiddleware that utilises the AppEngine User API
if is_remote_environment():
    MIDDLEWARE = [
        *MIDDLEWARE,
        "backend.core.middleware.GaeAuthenticationMiddleware",
    ]
else:
    MIDDLEWARE = [
        *MIDDLEWARE,
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]


ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# Database
# Use django-environ to parse the connection string
DATABASES = {"default": env.db()}

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432

# Use a in-memory sqlite3 database when testing if flag set
if os.getenv("USE_LOCAL_SQLITE_DB", None):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: 501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Use specialised Django User model that integrates with the AppEngine User API
AUTH_USER_MODEL = "core.BackendUser"

# Custom auth backend that utilises AppEngine's User API
AUTHENTICATION_BACKENDS = [
    "backend.core.backends.AppEngineUserAPIBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "static"))
STATIC_URL = "/static/"
STATICFILES_DIRS = []

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Integrations

# Mailerlite API
MAILERLITE_API_TOKEN = env("MAILERLITE_API_TOKEN")
MAILERLITE_GROUP = "bloxtest10"  # TODO: template here
