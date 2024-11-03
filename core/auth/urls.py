from django.urls import path
from core.auth.views import RegisterView, CustomTokenRefreshView, CustomTokenObtainPairView, VerifyUserView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('verify/', VerifyUserView.as_view(), name='verify'),
    path('logout/', LogoutView.as_view(), name='logout'),

]