from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from common.mixins import DynamicCacheMixin
from notification.models import Notification
from notification.serializers import NotificationSerializer


class NotificationViewSet(DynamicCacheMixin, viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

