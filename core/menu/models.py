from django.contrib.auth.models import Permission
from django.db import models

from core.user.models import CoreUser


# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(CoreUser, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=200, null=True, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='menu_items')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    class Meta:
        ordering = ['order']  # Order menu items by the `order` field

    def __str__(self):
        return self.name