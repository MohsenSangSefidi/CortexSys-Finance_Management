import pytest
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from transactions.models import TransactionModel

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        nickname='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    # Generate JWT token using PyJWT
    payload = {
        'user_id': user.id,
        'user_email': user.email,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }

    # Make sure to use your actual JWT secret key from settings
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    # Set the token in cookies as your view expects
    api_client.cookies['access_token'] = token
    return api_client


@pytest.fixture
def transaction(user):
    return TransactionModel.objects.create(
        title='Test Transaction',
        amount=100.00,
        type='income',
        date='2023-01-01',
        notes='Test notes',
        user=user
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        nickname='otheruser',
        email='other@example.com',
        password='testpass123'
    )


@pytest.fixture
def other_user_transaction(other_user):
    return TransactionModel.objects.create(
        title='Other User Transaction',
        amount=200.00,
        type='expense',
        date='2023-01-02',
        notes='Other user notes',
        user=other_user
    )
