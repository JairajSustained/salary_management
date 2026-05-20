import datetime
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.employees.models import Employee, EmploymentStatus


@pytest.fixture
def api_client():
	return APIClient()


@pytest.fixture
def insights_employees():
	"""
	Three USA employees (Engineering / Software Engineer) + one India employee
	(HR / HR Manager) with predictable salaries for calculation assertions.
	"""
	base = dict(date_of_joining=datetime.date.today(), employment_status="Active")
	return Employee.objects.bulk_create([
		Employee(first_name="Alice", last_name="A", job_title="Software Engineer", department="Engineering", country="USA",   salary=Decimal("40000.00"), **base),
		Employee(first_name="Bob",   last_name="B", job_title="Software Engineer", department="Engineering", country="USA",   salary=Decimal("60000.00"), **base),
		Employee(first_name="Carol", last_name="C", job_title="Software Engineer", department="Engineering", country="USA",   salary=Decimal("80000.00"), **base),
		Employee(first_name="Dave",  last_name="D", job_title="HR Manager",        department="HR",          country="India", salary=Decimal("50000.00"), **base),
	])


@pytest.mark.django_db
class TestEmployeeInsights:
	"""
	Tests for GET /api/employees/insights/
	"""

	def test_insights_returns_200(self, api_client, insights_employees):
		response = api_client.get(reverse("employee-insights"))
		assert response.status_code == 200

	def test_insights_response_has_by_country_key(self, api_client, insights_employees):
		response = api_client.get(reverse("employee-insights"))
		assert "by_country" in response.data

	def test_insights_response_has_by_department_key(self, api_client, insights_employees):
		response = api_client.get(reverse("employee-insights"))
		assert "by_department" in response.data

	def test_insights_response_has_by_title_key(self, api_client, insights_employees):
		response = api_client.get(reverse("employee-insights"))
		assert "by_title" in response.data

	def test_insights_by_country_entry_has_required_fields(self, api_client, insights_employees):
		response = api_client.get(reverse("employee-insights"))
		entry = next(e for e in response.data["by_country"] if e["country"] == "USA")
		assert "min_salary" in entry
		assert "max_salary" in entry
		assert "avg_salary" in entry
		assert "median_salary" in entry

	def test_insights_by_department_entry_has_required_fields(self, api_client, insights_employees):
		response = api_client.get(reverse("employee-insights"))
		entry = next(e for e in response.data["by_department"] if e["department"] == "Engineering")
		assert "min_salary" in entry
		assert "max_salary" in entry
		assert "avg_salary" in entry
		assert "median_salary" in entry

	def test_insights_by_title_entry_has_required_fields(self, api_client, insights_employees):
		response = api_client.get(reverse("employee-insights"))
		entry = next(e for e in response.data["by_title"] if e["job_title"] == "Software Engineer")
		assert "min_salary" in entry
		assert "max_salary" in entry
		assert "avg_salary" in entry
		assert "median_salary" in entry

	def test_insights_by_country_salary_calculations(self, api_client, insights_employees):
		# USA: [40000, 60000, 80000] → min=40000, max=80000, avg=60000, median=60000
		response = api_client.get(reverse("employee-insights"))
		usa = next(e for e in response.data["by_country"] if e["country"] == "USA")
		assert Decimal(usa["min_salary"]) == Decimal("40000.00")
		assert Decimal(usa["max_salary"]) == Decimal("80000.00")
		assert Decimal(usa["avg_salary"]) == Decimal("60000.00")
		assert Decimal(usa["median_salary"]) == Decimal("60000.00")

	def test_insights_by_department_salary_calculations(self, api_client, insights_employees):
		# Engineering: [40000, 60000, 80000] → min=40000, max=80000, avg=60000, median=60000
		response = api_client.get(reverse("employee-insights"))
		eng = next(e for e in response.data["by_department"] if e["department"] == "Engineering")
		assert Decimal(eng["min_salary"]) == Decimal("40000.00")
		assert Decimal(eng["max_salary"]) == Decimal("80000.00")
		assert Decimal(eng["avg_salary"]) == Decimal("60000.00")
		assert Decimal(eng["median_salary"]) == Decimal("60000.00")

	def test_insights_by_title_salary_calculations(self, api_client, insights_employees):
		# Software Engineer: [40000, 60000, 80000] → min=40000, max=80000, avg=60000, median=60000
		response = api_client.get(reverse("employee-insights"))
		eng = next(e for e in response.data["by_title"] if e["job_title"] == "Software Engineer")
		assert Decimal(eng["min_salary"]) == Decimal("40000.00")
		assert Decimal(eng["max_salary"]) == Decimal("80000.00")
		assert Decimal(eng["avg_salary"]) == Decimal("60000.00")
		assert Decimal(eng["median_salary"]) == Decimal("60000.00")

	def test_insights_excludes_inactive_employees(self, api_client, insights_employees):
		# Deactivate the 80000 employee; USA avg should shift to 50000, not 60000
		emp = Employee.objects.get(first_name="Carol")
		emp.employment_status = EmploymentStatus.INACTIVE
		emp.save()

		response = api_client.get(reverse("employee-insights"))
		usa = next(e for e in response.data["by_country"] if e["country"] == "USA")
		assert Decimal(usa["max_salary"]) == Decimal("60000.00")
