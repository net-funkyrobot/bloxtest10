import os

from google.appengine.api import wrap_wsgi_app

from backend.wsgi import application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings_remote")

app = wrap_wsgi_app(application)
