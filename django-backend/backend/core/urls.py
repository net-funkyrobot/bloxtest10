from django.urls import path

from backend.core import views

urlpatterns = [
    path("debug/", views.debug, name="debug"),
    path(
        "debug-raise-exception/",
        views.debug_raise_exception,
        name="debug_raise_exception",
    ),
    path("login_redirect/", views.login_redirect, name="gae_login_redirect"),
    path("switch_accounts/", views.switch_accounts, name="gae_switch_accounts"),
]
