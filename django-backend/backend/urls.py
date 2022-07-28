from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("ah/", include("djangae.urls")),
    path("googleauth/", include("djangae.contrib.googleauth.urls")),
    path("admin/", admin.site.urls),
]
