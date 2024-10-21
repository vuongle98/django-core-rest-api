from django.db import models
from core.user.models import CoreUser


class Notification(models.Model):
    # Notification types can be defined as choices
    NOTIFICATION_TYPES = (
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
    )

    user = models.ForeignKey(CoreUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Order notifications by creation time, most recent first

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}: {self.message[:20]}"
