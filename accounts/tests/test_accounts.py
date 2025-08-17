# tests/test_auth_views.py
import pytest
import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
class TestRegisterAccountView:
    def test_register_success(self, client):
        url = '/api/auth/register/'
        data = {
            "nickname": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123"
        }

        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['result'] is True
        assert response.data['message'] == "User created successfully."
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['email'] == data['email'].lower()
        assert response.data['data'][0]['nickname'] == data['nickname']

    def test_register_invalid_data(self, client):
        url = '/api/auth/register/'
        data = {
            "nickname": "",
            "email": "notanemail",
            "password": "123"
        }

        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['result'] is False
        assert response.data['message'] == "Invalid data"
        assert 'nickname' in response.data['data']
        assert 'email' in response.data['data']


@pytest.mark.django_db
class TestLoginAccountView:
    def test_login_success(self, client, test_user):
        url = '/api/auth/login/'
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }

        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] is True
        assert response.data['message'] == "Login successful"
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['email'] == test_user.email
        assert 'access_token' in response.data['data'][0]
        assert 'refresh_token' in response.data['data'][0]

        # Verify tokens are valid
        access_token = response.data['data'][0]['access_token']
        access_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        assert access_payload['user_id'] == test_user.id
        assert access_payload['token_type'] == "access_token"

        refresh_token = response.data['data'][0]['refresh_token']
        refresh_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        assert refresh_payload['user_id'] == test_user.id
        assert refresh_payload['token_type'] == "refresh_token"

    def test_login_user_not_found(self, client):
        url = '/api/auth/login/'
        data = {
            "email": "nonexistent@example.com",
            "password": "testpass123"
        }

        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['result'] is False
        assert response.data['message'] == "User does not exist"
        assert response.data['data'] == []

    def test_login_wrong_password(self, client, test_user):
        url = '/api/auth/login/'
        data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }

        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['result'] is False
        assert response.data['message'] == "Invalid password"
        assert response.data['data'] == []


@pytest.mark.django_db
class TestRefreshTokenView:
    def test_refresh_token_success(self, client, test_user):
        # login to get refresh token
        login_url = '/api/auth/login/'
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        login_response = client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['data'][0]['refresh_token']

        # test refresh
        refresh_url = '/api/auth/refresh/'  # Update with your actual URL
        client.cookies['refresh_token'] = refresh_token  # Set refresh_token
        response = client.post(
            refresh_url,
            format='json',
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] is True
        assert response.data['message'] == "Refresh token"
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['email'] == test_user.email
        assert 'access_token' in response.data['data'][0]
        assert 'refresh_token' in response.data['data'][0]

        # Verify new valid tokens
        new_access_token = response.data['data'][0]['access_token']
        new_access_payload = jwt.decode(new_access_token, settings.SECRET_KEY, algorithms=["HS256"])
        assert new_access_payload['user_id'] == test_user.id
        assert new_access_payload['token_type'] == "access_token"

        new_refresh_token = response.data['data'][0]['refresh_token']
        new_refresh_payload = jwt.decode(new_refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        assert new_refresh_payload['user_id'] == test_user.id
        assert new_refresh_payload['token_type'] == "refresh_token"

    def test_refresh_token_invalid_token(self, client):
        refresh_url = '/api/auth/refresh/'
        client.cookies['refresh_token'] = 'invalidtoken'
        response = client.post(
            refresh_url,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['result'] is False
        assert response.data['message'] == "Invalid token"
        assert response.data['data'] == []

    def test_refresh_token_wrong_token_type(self, client, test_user):
        # Create an access token instead of refresh token
        access_token_payload = {
            "token_type": "access_token",
            "user_id": test_user.id,
            "user_email": test_user.email,
            "iat": timezone.now(),
            "exp": timezone.now() + timezone.timedelta(days=1),
        }
        wrong_token = jwt.encode(
            access_token_payload, settings.SECRET_KEY, algorithm="HS256"
        )

        refresh_url = '/api/auth/refresh/'  # Update with your actual URL
        client.cookies['refresh_token'] = wrong_token
        response = client.post(
            refresh_url,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['result'] is False
        assert response.data['message'] == "Invalid token"
        assert response.data['data'] == []
