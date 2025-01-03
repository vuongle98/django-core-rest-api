from django.contrib import admin

# Register your models here.
from notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'message', 'is_read', 'created_at']
    list_filter = ['user', 'notification_type', 'is_read']
    search_fields = ['message']