from django.utils.timezone import now

from user.models import Profile


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            user = request.user
            print("middleware", user)

            user_profile = Profile.objects.get(user=user)
            user_profile.last_activity = now()
            user_profile.save(update_fields=['last_activity'])

        return response