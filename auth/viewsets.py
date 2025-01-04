
from django.contrib.auth.models import Permission, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from common.mixins import DynamicCacheMixin
from user.serializers import GroupSerializer, PermissionSerializer


class GroupViewSet(DynamicCacheMixin, viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class PermissionViewSet(DynamicCacheMixin, viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]