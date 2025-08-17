import pytest
from rest_framework import status
from transactions.models import TransactionModel

from accounts.models import UserModel


@pytest.mark.django_db
class TestTransactionView:

    def test_get_transactions_unauthenticated(self, api_client):
        response = api_client.get('/api/transactions/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['result'] is 'false'

    def test_get_transactions_authenticated_empty(self, authenticated_client, user):
        response = authenticated_client.get('/api/transactions/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] is True
        assert response.data['message'] == 'success'
        assert len(response.data['data']) == 0

    def test_get_transactions_with_data(self, authenticated_client, transaction):
        response = authenticated_client.get('/api/transactions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']) == 1
        assert response.data['data'][0]['title'] == 'Test Transaction'

    def test_create_transaction_success(self, authenticated_client):
        data = {
            'title': 'New Transaction',
            'amount': 150,
            'type': 'Expense',
            'date': '2023-01-02',
            'notes': 'New transaction notes'
        }
        response = authenticated_client.post('/api/transactions/', data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['result'] is True
        assert response.data['message'] == 'Transaction created'
        assert response.data['data'][0]['title'] == 'New Transaction'
        assert TransactionModel.objects.count() == 1

    def test_create_transaction_invalid_data(self, authenticated_client):
        data = {
            'title': '',  # Invalid empty title
            'amount': 'not_a_number',  # Invalid amount
            'type': 'invalid_type',  # Invalid type
        }
        response = authenticated_client.post('/api/transactions/', data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['result'] is False
        assert 'title' in response.data['data']
        assert 'amount' in response.data['data']
        assert 'type' in response.data['data']

    def test_update_transaction_success(self, authenticated_client, transaction):
        data = {
            'id': transaction.id,
            'title': 'Updated Title',
            'amount': 200,
        }
        response = authenticated_client.put('/api/transactions/', data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] is True
        assert response.data['message'] == 'Transaction updated'
        assert response.data['data'][0]['title'] == 'Updated Title'
        assert response.data['data'][0]['amount'] == 200

        # Verify the update in database
        transaction.refresh_from_db()
        assert transaction.title == 'Updated Title'
        assert transaction.amount == 200

    def test_update_transaction_not_found(self, authenticated_client):
        data = {
            'id': 999,  # Non-existent ID
            'title': 'Updated Title',
        }
        response = authenticated_client.put('/api/transactions/', data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['result'] is False
        assert response.data['message'] == 'Transaction does not exist'

    def test_update_transaction_belongs_to_other_user(self, authenticated_client, user):
        # Create another user and a transaction belonging to that user
        other_user = UserModel.objects.create_user(
            nickname='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        other_transaction = TransactionModel.objects.create(
            title='Other Transaction',
            amount=100.00,
            type='income',
            date='2023-01-01',
            notes='Other notes',
            user=other_user
        )

        data = {
            'id': other_transaction.id,
            'title': 'Updated Title',
        }
        response = authenticated_client.put('/api/transactions/', data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['result'] is False

    def test_delete_transaction_success(self, authenticated_client, transaction):
        data = {
            'id': transaction.id,
        }
        response = authenticated_client.delete('/api/transactions/', data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] is True
        assert response.data['message'] == 'Transaction deleted'
        assert TransactionModel.objects.count() == 0

    def test_delete_transaction_not_found(self, authenticated_client):
        data = {
            'id': 999,  # Non-existent ID
        }
        response = authenticated_client.delete('/api/transactions/', data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['result'] is False
        assert response.data['message'] == 'Transaction does not exist'

    def test_partial_update_transaction(self, authenticated_client, transaction):
        # Test that only provided fields are updated
        original_title = transaction.title
        original_notes = transaction.notes

        data = {
            'id': transaction.id,
            'amount': 300.00,
        }
        response = authenticated_client.put('/api/transactions/', data=data)
        assert response.status_code == status.HTTP_200_OK

        transaction.refresh_from_db()
        assert float(transaction.amount) == 300.00
        assert transaction.title == original_title  # Should remain unchanged
        assert transaction.notes == original_notes  # Should remain unchanged
