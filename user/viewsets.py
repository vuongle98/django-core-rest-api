from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from common.mixins import DynamicCacheMixin
from user.serializers import *


class UserViewSet(DynamicCacheMixin, viewsets.ModelViewSet):
    queryset = CoreUser.objects.all()
    serializer_class = CoreUserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class UserProfileViewSet(DynamicCacheMixin, viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class UserActivityLogViewSet(DynamicCacheMixin, viewsets.ModelViewSet):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]