from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from chat.models import Room
from chat.serializers import RoomSerializer, ChatMessageSerializer
from core.user.models import CoreUser


# Create your views here.
@login_required
def chat_room(request, room_name):
    return render(request, 'chat/chat_room.html', {
        'room_name': room_name
    })

# View to Create Room
class CreateRoomView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

# View to Add User to Room
class AddUserToRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        room = Room.objects.get(slug=slug)
        user = CoreUser.objects.get(username=request.data.get('username'))
        room.participants.add(user)
        return Response({"status": f"User {user.username} added to room {room.name}"}, status=status.HTTP_200_OK)

# View to Create Chat Message in a Room
class CreateChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        room = Room.objects.get(slug=slug)
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(room=room, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)