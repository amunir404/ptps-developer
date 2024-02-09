from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    User,
    UserPengawasTps,
    UserProfile,
    StartReport,
    EndReport,
    WhetherReport,
)
from django.db import models
from django.contrib.auth.admin import UserAdmin


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "fullname",
        "email",
        "username",
        "role",
        "is_active",
    )
    ordering = ("id",)


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserPengawasTps)
admin.site.register(StartReport)
admin.site.register(EndReport)
admin.site.register(WhetherReport)
