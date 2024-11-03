from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, \
    TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from core.user.models import CoreUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'password2']

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CoreUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        data['token'] = data.pop('access')
        data['refreshToken'] = data.pop('refresh')

        data.update({
            "type": "Bearer",
            "user": {
                "username": self.user.username,
                "email": self.user.email,
                "id": self.user.id
            }
        })

        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refreshToken = serializers.CharField(required=True, write_only=True)
    refresh = serializers.CharField(required=False, write_only=True)

    def validate(self, attrs):
        refresh_token = attrs.pop('refreshToken', None)

        if not refresh_token:
            raise serializers.ValidationError({'refreshToken': 'This field is required.'})

        # Call the parent class's validate method with the original field
        attrs['refresh'] = refresh_token

        data = super().validate(attrs)

        refresh = RefreshToken(attrs['refresh'])

        try:
            user = CoreUser.objects.get(id=refresh['user_id'])

            data["token"] = data.pop('access')

            data.update({
                "type": "Bearer",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "id": user.id
                }
            })
        except CoreUser.DoesNotExist:
            data['error'] = 'User not found'

        return data

class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    refreshToken = serializers.CharField(required=True, write_only=True)
    refresh = serializers.CharField(required=False, write_only=True)

    def validate(self, attrs):
        refresh_token = attrs.pop('refreshToken', None)
        if not refresh_token:
            raise serializers.ValidationError({'refreshToken': 'This field is required.'})

        # Call the parent class's validate method with the original field
        attrs['refresh'] = refresh_token
        return super().validate(attrs)

