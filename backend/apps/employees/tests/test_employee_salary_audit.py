import pytest
from decimal import Decimal

from django.db.models.deletion import ProtectedError
from django.urls import reverse
from rest_framework.test import APIClient

from apps.employees.models import EmployeeAudit


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
        client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"salary": "60000.00"},
            format="json",
        )
        employee.refresh_from_db()
        employee_audit = EmployeeAudit.objects.filter(employee=employee).all()
        assert employee_audit.count() == 1

    def test_employee_audit_new_salary_entry(self, employee):
        client = APIClient()
        client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"salary": "60000.00"},
            format="json",
        )
        employee.refresh_from_db()
        employee_audit = EmployeeAudit.objects.filter(employee=employee).latest("id")
        assert employee_audit.new_salary == Decimal("60000.00")

    def test_employee_audit_old_salary_is_captured(self, employee):
        original_salary = employee.salary
        client = APIClient()
        client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"salary": "60000.00"},
            format="json",
        )
        audit = EmployeeAudit.objects.filter(employee=employee).latest("id")
        assert audit.old_salary == original_salary

    def test_non_salary_update_does_not_create_audit(self, employee):
        client = APIClient()
        client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"job_title": "Senior Engineer"},
            format="json",
        )
        assert EmployeeAudit.objects.filter(employee=employee).count() == 0

    def test_multiple_salary_changes_create_multiple_audits(self, employee):
        client = APIClient()
        client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"salary": "60000.00"},
            format="json",
        )
        client.patch(
            reverse("employee-detail", args=[employee.id]),
            {"salary": "70000.00"},
            format="json",
        )
        assert EmployeeAudit.objects.filter(employee=employee).count() == 2


@pytest.mark.django_db
class TestEmployeeAuditModel:
    def test_audit_note_is_optional(self, employee):
        audit = EmployeeAudit.objects.create(
            employee=employee,
            old_salary=Decimal("50000.00"),
            new_salary=Decimal("60000.00"),
        )
        assert audit.note is None

    def test_deleting_employee_with_audit_is_blocked(self, employee):
        EmployeeAudit.objects.create(
            employee=employee,
            old_salary=Decimal("50000.00"),
            new_salary=Decimal("60000.00"),
        )
        with pytest.raises(ProtectedError):
            employee.delete()
