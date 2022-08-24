# flake8: noqa

import os

from backend.settings import BASE_DIR
from backend.settings_dev import *  # noqa: F401, F403

# Use a local SQLlite database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db_test.sqlite3"),
    }
}
