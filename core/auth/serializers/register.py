from rest_framework import serializers

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
