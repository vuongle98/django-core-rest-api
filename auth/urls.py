from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auth.views import RegisterView, CustomTokenRefreshView, CustomTokenObtainPairView, VerifyUserView
from auth.viewsets import GroupViewSet, PermissionViewSet

router = DefaultRouter()

router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('token/', CustomTokenObtainPairView.as_view(), name='token'),
    # path('token/refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('verify/', VerifyUserView.as_view(), name='verify'),
    path('', include('oauth2_provider.urls', namespace='oauth2_provider')),

]