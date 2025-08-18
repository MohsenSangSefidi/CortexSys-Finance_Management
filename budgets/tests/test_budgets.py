import pytest
from rest_framework import status
from budgets.models import BudgetModel


@pytest.mark.django_db
class TestBudgetView:
    def test_get_budgets_unauthenticated(self, client):
        response = client.get("/api/budgets/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["result"] is False

    def test_get_budgets_authenticated_empty(self, authenticated_client, user):
        response = authenticated_client.get("/api/budgets/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["result"] is True
        assert response.data["data"] == []

    def test_get_budgets_authenticated_with_data(self, authenticated_client, budget):
        response = authenticated_client.get("/api/budgets/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["result"] is True
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["title"] == "Test Budget"

    def test_create_budget_unauthenticated(self, client):
        data = {
            "title": "New Budget",
            "total_amount": 2000.00,
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
        }
        response = client.post("/api/budgets/", data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_budget_authenticated_invalid_data(self, authenticated_client):
        data = {
            "title": "",
            "total_amount": "not_a_number",
            "start_date": "invalid_date",
        }
        response = authenticated_client.post("/api/budgets/", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["result"] is False
        assert "title" in response.data["data"]
        assert "total_amount" in response.data["data"]
        assert "start_date" in response.data["data"]

    def test_create_budget_authenticated_valid_data(self, authenticated_client, user):
        data = {
            "title": "New Budget",
            "total_amount": 2000,
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
        }
        response = authenticated_client.post("/api/budgets/", data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["result"] is True
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["title"] == "New Budget"
        assert response.data["data"][0]["user"] == user.id

    def test_update_budget_unauthenticated(self, client, budget):
        data = {"id": budget.id, "title": "Updated Budget"}
        response = client.put("/api/budgets/", data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_budget_authenticated_invalid_data(self, authenticated_client):
        data = {"id": 999, "title": "Updated Budget"}
        response = authenticated_client.put("/api/budgets/", data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["result"] is False
        assert "Budget does not exist" in response.data["massage"]

    def test_update_budget_authenticated_valid_data(self, authenticated_client, budget):
        data = {"id": budget.id, "title": "Updated Budget", "total_amount": 1500.00}
        response = authenticated_client.put("/api/budgets/", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["result"] is True
        assert response.data["data"][0]["title"] == "Updated Budget"
        assert float(response.data["data"][0]["total_amount"]) == 1500.00

    def test_delete_budget_unauthenticated(self, client, budget):
        data = {"id": budget.id}
        response = client.delete("/api/budgets/", data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_budget_authenticated_invalid_id(self, authenticated_client):
        data = {"id": 999}
        response = authenticated_client.delete("/api/budgets/", data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["result"] is False
        assert "Budget does not exist" in response.data["massage"]

    def test_delete_budget_authenticated_valid_id(self, authenticated_client, budget):
        data = {"id": budget.id}
        response = authenticated_client.delete("/api/budgets/", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["result"] is True
        assert response.data["massage"] == "Deleted budget successfully"

        # Verify the budget deleted
        with pytest.raises(BudgetModel.DoesNotExist):
            BudgetModel.objects.get(id=budget.id)
