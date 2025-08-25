from utils.polls import authenticate_jwt_token
from rest_framework.response import Response
from rest_framework import views, status
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
import jwt

from .serializers import RegisterAccountSerializer, LoginAccountSerializer

from .models import UserModel


def create_token(user):
    # JWT Payload ( Preparing information for sent )
    access_token_payload = {
        "token_type": "access_token",
        "user_id": user.id,
        "user_email": user.email,
        "iat": timezone.now(),
        "exp": timezone.now() + timezone.timedelta(days=1),
    }
    refresh_token_payload = {
        "token_type": "refresh_token",
        "user_id": user.id,
        "user_email": user.email,
        "iat": timezone.now(),
        "exp": timezone.now() + timezone.timedelta(days=15),
    }

    # Create JWT token
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )

    return access_token, refresh_token


class RegisterAccountView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterAccountSerializer(data=request.data)

        # Validate data & return serializer error
        if not serializer.is_valid():
            return Response(
                {"result": False, "message": "Invalid data", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set serializer data
        nick_name = serializer.validated_data.get("nickname")
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        # Create account object
        try:
            user = UserModel.objects.create_user(
                nickname=nick_name,
                email=email.lower(),
            )
            user.set_password(password)
            user.save()
        except IntegrityError:
            return Response(
                {"result": False, "message": "User already exists", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Return response
        return Response(
            {
                "result": True,
                "message": "User created successfully.",
                "data": [
                    {
                        "id": user.id,
                        "nickname": user.nickname,
                        "email": user.email,
                    }
                ],
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAccountView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginAccountSerializer(data=request.data)

        # Validate data & return serializer error
        if not serializer.is_valid():
            return Response(
                {"result": False, "message": "Invalid data", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set serializer data
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        # Get user-object
        try:
            user = UserModel.objects.get(email=email.lower())
        except UserModel.DoesNotExist:
            return Response(
                {"result": False, "message": "User does not exist", "data": []},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check user password
        if not user.check_password(password):
            return Response(
                {"result": False, "message": "Invalid password", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create Token
        access_token, refresh_token = create_token(user)

        # Update last login date
        user.last_login = timezone.now()
        user.save()

        # Return success response
        return Response(
            {
                "result": True,
                "message": "Login successful",
                "data": [
                    {
                        "id": user.id,
                        "email": user.email,
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    }
                ],
            },
            status=status.HTTP_200_OK,
        )


class UserInfo(views.APIView):
    def get(self, request, *args, **kwargs):
        # Validate user authentications
        jwt_token = request.COOKIES.get("access_token")

        result, response, user = authenticate_jwt_token(jwt_token)

        if result:
            return response

        return Response(
            {
                "result": True,
                "message": "successfully",
                "data": [
                    {
                        "id": user.id,
                        "nickname": user.nickname,
                        "email": user.email,
                        "last_login": user.last_login,
                        "income": user.income(),
                        "expense": user.expense(),
                    }
                ],
            },
            status=status.HTTP_200_OK,
        )


class RefreshTokenView(views.APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        # Validate & Decode Access-Token
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
            )

            if not payload["token_type"] == "refresh_token":
                return Response(
                    {"result": False, "message": "Invalid token", "data": []},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except:
            return Response(
                {"result": False, "message": "Invalid token", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get User Information
        try:
            user = UserModel.objects.get(email=payload["user_email"])
        except UserModel.DoesNotExist:
            return Response(
                {"result": False, "message": "User does not exist", "data": []},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Create Token
        access_token, refresh_token = create_token(user)

        # Return response
        return Response(
            {
                "result": True,
                "message": "Refresh token",
                "data": [
                    {
                        "id": user.id,
                        "email": user.email,
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    }
                ],
            },
            status=status.HTTP_200_OK,
        )
