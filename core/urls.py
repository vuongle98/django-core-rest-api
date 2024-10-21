from django.urls import path, include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('notification/', include('core.notification.urls')),
    path('auth/', include('core.auth.urls'), name="auth"),
    path('users/', include('core.user.urls'), name='users'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]