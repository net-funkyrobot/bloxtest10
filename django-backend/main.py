import google.appengine.api

from backend.wsgi import application

app = google.appengine.api.wrap_wsgi_app(application)