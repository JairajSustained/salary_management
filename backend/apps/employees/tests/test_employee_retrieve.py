import uuid

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestEmployeeRetrieve:
    """
    Tests for GET /api/employees/{id}/
    """

    def test_employee_retrieve_returns_200(self, api_client, employee):
        response = api_client.get(reverse("employee-detail", args=[employee.id]))
        assert response.status_code == 200

    def test_employee_retrieve_returns_correct_employee(self, api_client, employee):
        response = api_client.get(reverse("employee-detail", args=[employee.id]))
        assert str(response.data["id"]) == str(employee.id)
        assert response.data["first_name"] == employee.first_name
        assert response.data["last_name"] == employee.last_name

    def test_employee_retrieve_nonexistent_returns_404(self, api_client):
        response = api_client.get(reverse("employee-detail", args=[uuid.uuid4()]))
        assert response.status_code == 404
