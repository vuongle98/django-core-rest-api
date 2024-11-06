from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from core.user.views import UserProfileView, UserSettingsView
from core.user.viewsets import *

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'profile', UserProfileViewSet)
router.register(r'activity', UserActivityLogViewSet)

router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('', include(router.urls)),
]