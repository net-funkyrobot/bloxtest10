# flake8: noqa
from backend.settings import *

# from backend.settings import (
#     ALLOWED_HOSTS,
#     AUTH_PASSWORD_VALIDATORS,
#     BASE_DIR,
#     DEFAULT_AUTO_FIELD,
#     INSTALLED_APPS,
#     MAILERLITE_API_TOKEN,
#     MIDDLEWARE,
#     LANGUAGE_CODE,
#     ROOT_URLCONF,
#     SECRET_KEY,
#     STATIC_ROOT,
#     STATIC_URL,
#     STATICFILES_DIRS,
#     TEMPLATES,
#     TIME_ZONE,
#     USE_I18N,
#     USE_L10N,
#     USE_TZ,
#     WSGI_APPLICATION,
#     get_secrets,
# )

# Integrations

# Set MAILERLITE_GROUP to "testing" so test contacts don't pollute the mailing list
MAILERLITE_GROUP = "testing"
