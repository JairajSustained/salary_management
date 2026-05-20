import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.employees.models import Employee, EmploymentStatus


@pytest.fixture
def api_client():
	return APIClient()


@pytest.mark.django_db
class TestEmployeeDelete:
	"""
	Tests for DELETE /api/employees/{id}/ — soft delete (marks inactive)
	"""

	def test_employee_delete_returns_204(self, api_client, employee):
		response = api_client.delete(reverse("employee-detail", args=[employee.id]))
		assert response.status_code == 204

	def test_employee_delete_is_soft_delete(self, api_client, employee):
		api_client.delete(reverse("employee-detail", args=[employee.id]))
		employee.refresh_from_db()
		assert employee.employment_status == EmploymentStatus.INACTIVE

	def test_employee_delete_does_not_remove_from_db(self, api_client, employee):
		api_client.delete(reverse("employee-detail", args=[employee.id]))
		assert Employee.objects.filter(id=employee.id).exists()
