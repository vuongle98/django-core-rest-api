from django.db import models
from django.utils.text import slugify
from core.user.models import CoreUser

# Create your models here.

class Room(models.Model):
    ROOM_CHOICES = [
        ('GLOBAL', 'GLOBAL'),
        ('PRIVATE', 'PRIVATE'),
        ('GROUP', 'GROUP'),
    ]
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(CoreUser)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(CoreUser, related_name='creator', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    type = models.CharField(max_length=100, choices=ROOM_CHOICES)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save()


class ChatMessage(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(CoreUser, on_delete=models.CASCADE)
    content = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'

    @staticmethod
    def message_read_true(message_id):
        msg_inst = ChatMessage.objects.filter(id=message_id).first()
        msg_inst.read = True
        msg_inst.save()
        return None

    @staticmethod
    def all_msg_read(room_id, username):
        all_msg = ChatMessage.objects.filter(room_id=room_id, read=False).exclude(
            user__username=username)
        for msg in all_msg:
            msg.read = True
            msg.save()
        return None

    @staticmethod
    def count_by_room(room_id):
        return ChatMessage.objects.filter(room_id=room_id).count()