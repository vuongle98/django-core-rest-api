from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def access_token_generator(request):
    user = request.user  # Access the authenticated user from the request object
    return str(AccessToken.for_user(user))

def refresh_token_generator(request):
    user = request.user
    return str(RefreshToken.for_user(user))