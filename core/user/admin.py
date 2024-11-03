from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

from core.user.models import *


# Register your models here.
@admin.register(CoreUser)
class CoreUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'email']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'avatar']
    list_filter = ['user']

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(UserActivityLog)
class UserAccessLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'path', 'ip_address', 'timestamp', 'user_agent', 'method', 'resource', 'status']
    list_filter = ['user', 'action', 'timestamp']
    search_fields = ['user__username', 'ip_address']

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass

@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    pass

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass