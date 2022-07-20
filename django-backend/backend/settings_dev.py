import os

from backend.settings import BASE_DIR
from backend.settings_staging import *  # noqa: F401, F403

DEBUG = True

# Use a local SQLlite database like settings_test but specify a different
# sqlite file
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
