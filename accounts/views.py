from django.db import IntegrityError
from rest_framework import views, status
from rest_framework.response import Response

from .serializers import RegisterAccountSerializer

from .models import UserModel


class RegisterAccountView(views.APIView):
    def post(self, request, *args, **kwargs):

        serializer = RegisterAccountSerializer(data=request.data)

        # Validate data & return serializer error
        if not serializer.is_valid():
            return Response(
                {
                    'result': False,
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )

        # Ser serializer data
        nick_name = serializer.validated_data.get('nickname')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        # Create account object
        user = UserModel.objects.create_user(
            nickname=nick_name,
            email=email,
        )
        user.set_password(password)

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
