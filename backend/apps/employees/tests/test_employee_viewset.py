import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.employees.models import Employee


@pytest.fixture
def api_client():
	return APIClient()


@pytest.fixture
def bulk_employees(employee_data):
	employees = [
		Employee(**{**employee_data, "first_name": f"User{i}"})
		for i in range(25)
	]
	return Employee.objects.bulk_create(employees)


@pytest.mark.django_db
class TestEmployeeViewset:
	"""
	Tests for Employee Viewset: List, Creation, Retrieve
	"""

	def test_employee_list_status_code(self, api_client):
		response = api_client.get(reverse("employee-list"))
		assert response.status_code == 200

	def test_employee_list_response_is_paginated(self, api_client):
		response = api_client.get(reverse("employee-list"))
		assert "count" in response.data
		assert "next" in response.data
		assert "previous" in response.data
		assert "results" in response.data

	def test_employee_list_results_is_a_list(self, api_client):
		response = api_client.get(reverse("employee-list"))
		assert isinstance(response.data["results"], list)

	def test_employee_list_next_page_exists_when_results_exceed_page_size(
		self, api_client, bulk_employees
	):
		response = api_client.get(reverse("employee-list"))
		assert response.data["count"] == 25
		assert response.data["next"] is not None
