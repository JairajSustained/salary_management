from io import StringIO

import pytest
from django.core.management import call_command, CommandError

from apps.employees.models import Employee, EmploymentStatus


@pytest.mark.django_db
class TestEmployeeSeedCommand:
    """
    Tests for: python manage.py seed_employees
    """

    def test_seed_command_exists(self):
        try:
            call_command("seed_employees", stdout=StringIO())
        except CommandError:
            pytest.fail("seed_employees command raised CommandError")

    def test_seed_command_creates_10000_employees(self):
        call_command("seed_employees", stdout=StringIO())
        assert Employee.objects.count() == 10_000

    def test_seed_command_all_employees_are_active(self):
        call_command("seed_employees", stdout=StringIO())
        inactive_count = Employee.objects.filter(
            employment_status=EmploymentStatus.INACTIVE
        ).count()
        assert inactive_count == 0

    def test_seed_command_employees_have_non_empty_names(self):
        call_command("seed_employees", stdout=StringIO())
        assert not Employee.objects.filter(first_name="").exists()
        assert not Employee.objects.filter(last_name="").exists()

    def test_seed_command_employees_have_non_empty_job_fields(self):
        call_command("seed_employees", stdout=StringIO())
        assert not Employee.objects.filter(job_title="").exists()
        assert not Employee.objects.filter(department="").exists()
        assert not Employee.objects.filter(country="").exists()

    def test_seed_command_employees_have_positive_salary(self):
        call_command("seed_employees", stdout=StringIO())
        assert not Employee.objects.filter(salary__lte=0).exists()

    def test_seed_command_outputs_success_message(self):
        out = StringIO()
        call_command("seed_employees", stdout=out)
        assert "10000" in out.getvalue() or "10,000" in out.getvalue()

    def test_seed_command_employees_have_varied_countries(self):
        call_command("seed_employees", stdout=StringIO())
        country_count = Employee.objects.values("country").distinct().count()
        assert country_count > 1

    def test_seed_command_employees_have_varied_departments(self):
        call_command("seed_employees", stdout=StringIO())
        department_count = Employee.objects.values("department").distinct().count()
        assert department_count > 1
