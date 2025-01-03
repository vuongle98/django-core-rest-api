from django.contrib.auth import user_logged_out
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from user.models import UserActivityLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    # Get the user's IP address
    ip = request.META.get('REMOTE_ADDR')

    # Get the user-agent string (browser and device info)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    method = request.META.get('REQUEST_METHOD')

    # Create a log entry
    UserActivityLog.objects.create(
        user=user,
        ip_address=ip,
        method=method,
        user_agent=user_agent,
        action='login',
        status='success',
        resource='site'
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    # Get the user-agent string (browser and device info)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    method = request.META.get('REQUEST_METHOD')
    ip = request.META.get('REMOTE_ADDR')

    UserActivityLog.objects.create(
        user=user,
        ip_address=ip,
        user_agent=user_agent,
        method=method,
        action='logout',
        status='success',
        resource='site'
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip