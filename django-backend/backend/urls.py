from django.contrib import admin
from django.urls import include, path

from .api_v1 import api, openapi_yaml

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include(("backend.core.urls", "core"), namespace="core")),
    path("api-v1/", api.urls),
    path("api-v1/openapi.yaml", openapi_yaml),
]
