from django.contrib import admin

from backend.core.models import AdminUser, MobileAppUser

admin.site.register(AdminUser)
admin.site.register(MobileAppUser)
