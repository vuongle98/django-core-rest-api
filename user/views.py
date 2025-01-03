from django.contrib.auth.models import Permission
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from menu.models import MenuItem
from menu.serializers import MenuItemSerializer
from user.models import Profile, UserSettings
from user.pagination import MenuPagination
from user.serializers import UserProfileSerializer, UserSettingsSerializer


# Create your views here.
class UserProfileView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            profile = Profile.objects.get(user__id=user.id)

            return Response(UserProfileSerializer(profile).data)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserSettingsView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            settings = UserSettings.objects.get(user__id=user.id)

            return Response(UserSettingsSerializer(settings).data)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class MenuItemView(views.APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = MenuPagination

    def get(self, request):
        user = request.user

        perms = user.user_permissions.all() | Permission.objects.filter(group__user=user)
        # perms = user.get_all_permissions()
        # print(perms)
        menu_items = MenuItem.objects.filter(permissions__in=perms) | MenuItem.objects.filter(permissions__isnull=True)

        # Get all menu items that the user has permission for

        # paginator = self.pagination_class()
        # paginated_menu_items = paginator.paginate_queryset(menu_hierarchy, request)
        # serializer = MenuItemSerializer(paginated_menu_items, many=True)

        return Response(MenuItemSerializer(menu_items, many=True).data)

    def build_menu_hierarchy(self, menus):
        # Recursively build the menu structure, assuming parent-child relationships
        menu_dict = {}
        for menu in menus:
            if menu.parent is None:
                menu_dict[menu] = self.get_children(menu, menus)
        return menu_dict

    def get_children(self, parent_menu, all_menus):
        # Get the children for a given parent
        children = [menu for menu in all_menus if menu.parent == parent_menu]
        return children