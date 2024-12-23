from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from core.user.views import UserProfileView, UserSettingsView, MenuItemView
from core.user.viewsets import *

router = DefaultRouter()

router.register(r'profile', UserProfileViewSet)
router.register(r'activity', UserActivityLogViewSet)

router.register(r'', UserViewSet)

urlpatterns = [
    # path('profile/', UserProfileView.as_view(), name='profile'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('menu-items/', MenuItemView.as_view(), name='menu-item'),
    path('', include(router.urls)),
]