from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings


User = get_user_model()


def create_jwt_response(username):
    """"
    Create JWT response to provide token to
    frontend when OTP verified
    """
    user = User.objects.get(username=username)
    JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
    JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
    # JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER

    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_access_token = JWT_ENCODE_HANDLER(payload)
    # login(request, user) # Not required when JWT is used
    response = {
        # 'token_type': api_settings.JWT_AUTH_HEADER_PREFIX,
        'access_token': jwt_access_token,
        # 'id': user.id,
        # 'username': user.username,
        # 'expired_at': JWT_DECODE_HANDLER(jwt_access_token)['exp']
    }
    return response
