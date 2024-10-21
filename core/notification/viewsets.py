from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.notification.models import Notification
from core.notification.serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

