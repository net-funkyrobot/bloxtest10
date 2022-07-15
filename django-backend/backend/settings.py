import io
import os
from urllib.parse import urlparse

import environ
from google.cloud import secretmanager

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, '.env')

if os.path.isfile(env_file):
    # Use a local secret file, if provided
    env.read_env(env_file)

elif os.getenv('TRAMPOLINE_CI', None):
    # Create local settings if running with CI, for unit testing
    placeholder = (
        'SECRET_KEY=a\n'
        'DATABASE_URL=sqlite://{db_path}'.format(db_path=os.path.join(BASE_DIR, 'db_test.sqlite3'))
    )
    env.read_env(io.StringIO(placeholder))

elif os.environ.get('GOOGLE_CLOUD_PROJECT', None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get('SETTINGS_NAME', 'backend_settings')
    name = f'projects/{project_id}/secrets/{settings_name}/versions/latest'
    payload = client.access_secret_version(name=name).payload.data.decode('UTF-8')
    env.read_env(io.StringIO(payload))

else:
    raise Exception('No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.')

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Change this to 'False' when you are ready for production
DEBUG = env('DEBUG')

# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to App Engine. This code takes the URL and converts it to both these settings formats.
APPENGINE_URL = env('APPENGINE_URL', default=None)
if APPENGINE_URL:
    # Ensure a scheme is present in the URL before it's processed.
    if not urlparse(APPENGINE_URL).scheme:
        APPENGINE_URL = f'https://{APPENGINE_URL}'

    ALLOWED_HOSTS = [urlparse(APPENGINE_URL).netloc]    # noqa: WPS407
    CSRF_TRUSTED_ORIGINS = [APPENGINE_URL]    # noqa: WPS407
    SECURE_SSL_REDIRECT = True
else:
    ALLOWED_HOSTS = ['*']    # noqa: WPS407

# Application definition

INSTALLED_APPS = [    # noqa: WPS407
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend.core',
]

MIDDLEWARE = [    # noqa: WPS407
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [    # noqa: WPS407
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# Use django-environ to parse the connection string
DATABASES = {'default': env.db()}    # noqa: WPS407

# If the flag as been set, configure to use proxy
if os.getenv('USE_CLOUD_SQL_AUTH_PROXY', None):
    DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES['default']['PORT'] = 5432

# Use a in-memory sqlite3 database when testing in CI systems or if flag set
# TODO(glasnt) CHECK IF THIS IS REQUIRED because we're setting a val above
if os.getenv('TRAMPOLINE_CI', None) or os.getenv('USE_LOCAL_SQLITE_DB', None):
    DATABASES = {    # noqa: WPS407
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation

AUTH_PASSWORD_VALIDATORS = [    # noqa: WPS407
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',    # noqa: 501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',    # noqa: 501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',    # noqa: 501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',    # noqa: 501
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = []    # noqa: WPS407

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
