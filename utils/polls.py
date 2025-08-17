from rest_framework.response import Response
from accounts.models import UserModel
from django.conf import settings
from rest_framework import status
import jwt


# A Function For Validating User Access-Token And Return User Object
def authenticate_jwt_token(jwt_token):
    response = Response()

    # Validate & Decode Access-Token
    try:
        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])

    except:
        # Set Response Data
        response.data = {
            'result': 'false',
            'message': 'invalid_token or expired',
            'data': []
        }
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return True, response, None

    # Get User Information
    try:
        user = UserModel.objects.get(email=payload['user_email'])
    except UserModel.DoesNotExist:
        response.data = {
            'result': 'false',
            'message': 'user does not exist',
            'data': []
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return True, response

    return False, response, user
