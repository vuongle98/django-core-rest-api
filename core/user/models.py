from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.timezone import now


class CoreUser(AbstractUser):
    pass

    def __str__(self):
        return self.username or self.email

class Profile(models.Model):
    user = models.OneToOneField(CoreUser, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True, validators=[MaxValueValidator(now().date())])
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class UserActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view', 'View'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('error', 'Error'),
        ('other', 'Other'),
        # Add more actions as needed
    ]

    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ]

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('error', 'Error')
    ]

    user = models.ForeignKey(CoreUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=256, null=True, blank=True)
    resource = models.CharField(max_length=255, null=True, blank=True)  # e.g., the resource being accessed or modified
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)  # success, failure, error
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES)  # HTTP method (GET, POST, etc.)
    body = models.JSONField(null=True, blank=True)  # Store additional data (e.g., form input)
    query = models.JSONField(null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user} performed {self.action} on {self.resource} at {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']