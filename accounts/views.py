from django.conf import settings
from rest_framework.response import Response
from rest_framework import views, status
from django.utils import timezone

import jwt

from .serializers import RegisterAccountSerializer, LoginAccountSerializer

from .models import UserModel


class RegisterAccountView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterAccountSerializer(data=request.data)

        # Validate data & return serializer error
        if not serializer.is_valid():
            return Response(
                {
                    'result': False,
                    'message': 'Invalid data',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )

        # Set serializer data
        nick_name = serializer.validated_data.get('nickname')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        # Create account object
        user = UserModel.objects.create_user(
            nickname=nick_name,
            email=email,
        )
        user.set_password(password)
        user.save()

        # Return response
        return Response(
            {
                'result': True,
                'message': 'User created successfully.',
                'data': [
                    {
                        'id': user.id,
                        'nickname': user.nickname,
                        'email': user.email,
                    }
                ]
            }, status=status.HTTP_201_CREATED
        )


class LoginAccountView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginAccountSerializer(data=request.data)

        # Validate data & return serializer error
        if not serializer.is_valid():
            return Response(
                {
                    'result': False,
                    'message': 'Invalid data',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )

        # Set serializer data
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        # Get user-object
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response(
                {
                    'result': False,
                    'message': 'User does not exist',
                    'data': []
                }, status=status.HTTP_404_NOT_FOUND
            )

        # Check user password
        if not user.check_password(password):
            return Response(
                {
                    'result': False,
                    'message': 'Invalid password',
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST
            )

        # JWT Payload ( Preparing information for sent )
        payload = {
            'user_id': user.id,
            'user_email': user.email,
            'iat': timezone.now(),
            'exp': timezone.now() + timezone.timedelta(days=1),
        }

        # Create JWT token
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        # Update last login date
        user.last_login = timezone.now()
        user.save()

        # Return success response
        return Response(
            {
                'result': True,
                'message': 'Login successful',
                'data': [
                    {
                        'id': user.id,
                        'email': user.email,
                        'JWT_token': token,
                    }
                ]
            }, status=status.HTTP_200_OK
        )
