from rest_framework_jwt.settings import api_settings



def jwt_response_payload_handler(token, user=None, request=None):
    from src.profiles.api.serializers import UserSerializer
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

def create_token_from_payload(payload=None):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(payload)
    token = jwt_encode_handler(payload)
    return token