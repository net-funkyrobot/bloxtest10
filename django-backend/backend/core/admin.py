from django.contrib import admin

from backend.core.models import BackendUser, MobileAppUser


admin.site.register(BackendUser)
admin.site.register(MobileAppUser)
