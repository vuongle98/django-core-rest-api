from django.contrib import admin

from chat.models import Room, ChatMessage


# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass