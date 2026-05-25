import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.employees.models import Employee


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestEmployeeCreate:
    """
    Tests for POST /api/employees/
    """

    def test_employee_create_returns_201(self, api_client, employee_data):
        response = api_client.post(
            reverse("employee-list"), employee_data, format="json"
        )
        assert response.status_code == 201

    def test_employee_create_saves_to_db(self, api_client, employee_data):
        api_client.post(reverse("employee-list"), employee_data, format="json")
        assert Employee.objects.count() == 1

    def test_employee_create_response_contains_id(self, api_client, employee_data):
        response = api_client.post(
            reverse("employee-list"), employee_data, format="json"
        )
        assert "id" in response.data

    def test_employee_create_with_missing_required_field_returns_400(
        self, api_client, employee_data
    ):
        del employee_data["first_name"]
        response = api_client.post(
            reverse("employee-list"), employee_data, format="json"
        )
        assert response.status_code == 400
