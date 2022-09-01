from django.urls import path

from backend.core import views

urlpatterns = [
    path("debug/", views.debug, name="debug"),
    path(
        "debug-raise-exception/",
        views.debug_raise_exception,
        name="debug_raise_exception",
    ),
    path("deferred/", views.deferred_handler, name="tasks_deferred_handler"),
]
