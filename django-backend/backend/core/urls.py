from django.conf.urls import path

from backend.core import views

urlpatterns = [
    path("login_redirect/", views.login_redirect, name="gae_login_redirect"),
    path("switch_accounts/", views.switch_accounts, name="gae_switch_accounts"),
]
