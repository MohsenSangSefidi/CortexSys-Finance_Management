import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

UserModel = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def test_user():
    return UserModel.objects.create_user(
        nickname="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def authenticated_client(client, test_user):
    # First login to get tokens
    login_url = "/api/login/"
    login_data = {"email": "test@example.com", "password": "testpass123"}
    response = client.post(login_url, login_data, format="json")

    # Set cookies for authenticated requests
    client.cookies = response.cookies
    return client
