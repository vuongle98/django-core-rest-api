from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from core.user.viewsets import *

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'profile', UserProfileViewSet)
router.register(r'activity', UserActivityLogViewSet)

router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)


urlpatterns = [
    path('', include(router.urls)),

]