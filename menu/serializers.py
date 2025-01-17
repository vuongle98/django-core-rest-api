from rest_framework import serializers

from menu.models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'path', 'icon', 'order', 'children')

    def get_children(self, obj):
        # Recursively get children for the menu item
        return MenuItemSerializer(obj.children.all(), many=True).data