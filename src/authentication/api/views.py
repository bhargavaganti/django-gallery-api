from rest_framework_jwt.settings import api_settings



def jwt_response_payload_handler(token, user=None, request=None):
    """
    Прегажена метода из JWT Token Authentication пакета;
    позива се када се приступи /api/auth/token
    Форматира приказ
    :param token:
    :param user:
    :param request:
    :return: dict
    """

    from src.profiles.api.serializers import UserSerializer

    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


def create_token_from_payload(payload=None):
    """
    Прегажена метода из JWT Token Authentication пакета;
    Користи се за кеирање токена из задате промењиве

    :param payload:
    :return:  dict
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler  = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(payload)
    token = jwt_encode_handler(payload)
    return token
