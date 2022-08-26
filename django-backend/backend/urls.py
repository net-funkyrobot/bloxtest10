from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include(("backend.core.urls", "core"), namespace="core")),
]
