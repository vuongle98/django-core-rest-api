from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from common.mixins import DynamicCacheMixin
from menu.models import MenuItem
from menu.serializers import MenuItemSerializer


class MenuItemViewSet(DynamicCacheMixin, viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]