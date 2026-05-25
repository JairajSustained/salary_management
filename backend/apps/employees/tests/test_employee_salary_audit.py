import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.employees.models import EmployeeAudit
from decimal import Decimal

@pytest.mark.django_db
class TestEmployeeSalaryUpdate:
	"""
	Checks for Employee Audit for salary
	"""

	def test_employee_update_salary_audit_entry(self, employee):
		"""
		Tests whether updating the salary, it creates an audit entry or not.
		"""
		client = APIClient()
		client.patch(reverse("employee-detail", args=[employee.id]), {"salary": "60000.00"}, format="json")
		employee.refresh_from_db()
		employee_audit = EmployeeAudit.objects.filter(employee=employee).all()
		assert employee_audit.count() == 1

	def test_employee_audit_new_salary_entry(self, employee):
		client = APIClient()
		client.patch(reverse("employee-detail", args=[employee.id]), {"salary": "60000.00"}, format="json")
		employee.refresh_from_db()
		employee_audit = EmployeeAudit.objects.filter(employee=employee).latest("id")
		assert employee_audit.new_salary == Decimal(60000.00)
	


