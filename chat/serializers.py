from rest_framework import serializers
from .models import Room, ChatMessage
from core.user.models import CoreUser

class RoomSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(
        many=True,
        queryset=CoreUser.objects.all(),
        slug_field='username',
        required=False
    )
    creator = serializers.SlugRelatedField(
        queryset=CoreUser.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Room
        fields = ['id', 'name', 'participants', 'creator', 'active', 'avatar', 'type', 'slug']
        read_only_fields = ['created_at', 'updated_at', 'slug']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        queryset=CoreUser.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'content', 'created_at', 'read']
        read_only_fields = ['created_at', 'received_at']