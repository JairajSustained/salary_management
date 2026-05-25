import uuid

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestEmployeePatch:
    """
    Tests for PATCH /api/employees/{id}/
    """

    def test_employee_patch_returns_200(self, api_client, employee):
        response = api_client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"salary": "60000.00"},
            format="json",
        )
        assert response.status_code == 200

    def test_employee_patch_updates_field(self, api_client, employee):
        api_client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"salary": "60000.00"},
            format="json",
        )
        employee.refresh_from_db()
        assert employee.salary == 60000.00

    def test_employee_patch_does_not_overwrite_other_fields(self, api_client, employee):
        original_first_name = employee.first_name
        api_client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"salary": "60000.00"},
            format="json",
        )
        employee.refresh_from_db()
        assert employee.first_name == original_first_name

    def test_employee_patch_nonexistent_returns_404(self, api_client):
        response = api_client.patch(
            reverse("employee-detail", args=[uuid.uuid4()]),
            {"salary": "60000.00"},
            format="json",
        )
        assert response.status_code == 404

    def test_employee_patch_returns_updated_data(self, api_client, employee):
        response = api_client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"job_title": "Senior Engineer"},
            format="json",
        )
        assert response.data["job_title"] == "Senior Engineer"
