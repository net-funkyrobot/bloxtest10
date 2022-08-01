import os

from backend.wsgi import application
from google.appengine.api import wrap_wsgi_app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = wrap_wsgi_app(application)
