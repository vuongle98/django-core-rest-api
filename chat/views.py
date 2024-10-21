from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def chat_room(request, room_name):
    return render(request, 'chat/chat_room.html', {
        'room_name': room_name
    })