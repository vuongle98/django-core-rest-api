from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.user.models import Profile, UserSettings
from core.user.serializers import UserProfileSerializer, UserSettingsSerializer


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