from django.contrib import admin

from backend.core.models import GaeUser, MobileAppUser


admin.site.register(GaeUser)
admin.site.register(MobileAppUser)
