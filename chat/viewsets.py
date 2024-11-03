from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from chat.models import Room
from chat.serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'  # Use 'slug' instead of the default 'pk'

    def perform_create(self, serializer):
        # Automatically set the creator as the user making the request
        serializer.save(creator=self.request.user)