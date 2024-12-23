from django.contrib.auth.models import Permission, Group

from core.user.models import UserActivityLog, CoreUser, Profile, UserSettings
from rest_framework import serializers

class CoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'is_active', 'date_joined']  # 'id', 'is_active', and 'date_joined' are read-only
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CoreUser(**validated_data)  # Create a User instance without saving
        user.set_password(validated_data['password'])  # Hash the password
        user.save()  # Now save the User instance
        return user

class CoreUserEmbeddedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'is_active', 'date_joined']  # 'id', 'is_active', and 'date_joined' are read-only

class UserProfileSerializer(serializers.ModelSerializer):
    user = CoreUserEmbeddedSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'avatar', 'address', 'date_of_birth', 'phone_number', 'is_verified', 'is_online']

class UserSettingsSerializer(serializers.ModelSerializer):
    user = CoreUserEmbeddedSerializer(read_only=True)

    class Meta:
        model = UserSettings
        fields = ['id', 'dark_mode', 'user']

# Serializer for updating user info
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['username', 'email', 'first_name', 'last_name']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class UserActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CoreUser.objects.all(), source='user')

    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'user_id', 'action', 'timestamp', 'resource', 'status', 'ip_address', 'method', 'body', 'query']