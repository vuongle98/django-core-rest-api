from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.menu.models import MenuItem
from core.menu.serializers import MenuItemSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]