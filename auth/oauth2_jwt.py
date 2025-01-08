from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def access_token_generator(request):
    user = request.user  # Access the authenticated user from the request object
    if user:
        token = AccessToken.for_user(user)
        token["username"] = user.username
        return str(token)

    token = AccessToken()
    token["username"] = "service"
    return str(token)

def refresh_token_generator(request):
    user = request.user

    if user:
        token = RefreshToken.for_user(user)
        token["username"] = user.username
        return str(token)

    token = RefreshToken()
    token["username"] = "service"
    return str(token)