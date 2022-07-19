from django.contrib import admin

from backend.core.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass    # noqa: WPS420 WPS604


admin.site.register(UserProfile, UserProfileAdmin)
