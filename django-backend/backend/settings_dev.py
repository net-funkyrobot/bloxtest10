import os

from backend.settings_staging import *  # noqa: F401, F403

DEBUG = True

MIDDLEWARE.append("djangae.contrib.googleauth.middleware.LocalIAPLoginMiddleware")
