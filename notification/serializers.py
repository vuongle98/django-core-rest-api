from rest_framework import serializers

from notification.models import Notification
from user.models import CoreUser

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.PrimaryKeyRelatedField(queryset=CoreUser.objects.all(), source='user')

    class Meta:
        model = Notification
        fields = ['id', 'user', 'user_id', 'notification_type', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'user', 'user_id', 'created_at']  # Prevent users from modifying these fields
