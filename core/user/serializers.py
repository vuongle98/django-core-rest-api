from django.contrib.auth.models import Permission, Group

from core.user.models import UserActivityLog, CoreUser, Profile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'is_active', 'date_joined']  # 'id', 'is_active', and 'date_joined' are read-only

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# Serializer for updating user info
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['username', 'email', 'first_name', 'last_name']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class UserActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CoreUser.objects.all(), source='user')

    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'user_id', 'action', 'timestamp', 'resource', 'status', 'ip_address', 'method', 'body', 'query']