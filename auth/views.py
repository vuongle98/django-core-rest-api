from rest_framework import views, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from auth.serializers import RegisterSerializer, CustomTokenObtainPairSerializer, \
    CustomTokenRefreshSerializer, CustomTokenBlacklistSerializer

from user.models import CoreUser


# Create your views here.
class RegisterView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    queryset = CoreUser.objects.all()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class VerifyUserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth_user = request.user

        return Response({
            "username": auth_user.username,
            "email": auth_user.email,
            "id": auth_user.id,
        }, status=status.HTTP_200_OK)

class LogoutView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]

    # must add authentication classes
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = CustomTokenBlacklistSerializer