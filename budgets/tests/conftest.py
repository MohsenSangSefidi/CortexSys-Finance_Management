import pytest
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from budgets.models import BudgetModel

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        nickname="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def authenticated_client(client, user):
    # Generate JWT token using PyJWT
    payload = {
        "user_id": user.id,
        "user_email": user.email,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
    }

    # Make sure to use your actual JWT secret key from settings
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    client.cookies["access_token"] = str(token)
    return client


@pytest.fixture
def budget(user):
    return BudgetModel.objects.create(
        title="Test Budget",
        total_amount=1000,
        start_date="2023-01-01",
        end_date="2023-12-31",
        user=user,
    )
