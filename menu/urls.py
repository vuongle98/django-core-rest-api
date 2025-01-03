from django.urls import path, include
from rest_framework.routers import DefaultRouter

from menu.viewsets import MenuItemViewSet

router = DefaultRouter()
router.register(r'', MenuItemViewSet)


urlpatterns = [
    path('', include(router.urls)),

]