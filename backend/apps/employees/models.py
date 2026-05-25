from django.core.validators import MinValueValidator
from django.db import models
import uuid


class EmploymentStatus(models.TextChoices):
    ACTIVE = "Active", "Active"
    INACTIVE = "Inactive", "Inactive"


class Employee(models.Model):
    """
    Represents an employee in the organization.
    Used by HR Managers to manage employee data and salary insights.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100, help_text="Department of the employee")
    country = models.CharField(max_length=100, help_text="Country of the employee")
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text="Salary of the employee in USD",
    )
    date_of_joining = models.DateField(help_text="Date of joining of the employe")
    employment_status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
        help_text="Employment status of the employee",
    )

    class Meta:
        db_table = "employees"
        indexes = [
            models.Index(fields=["first_name", "last_name"], name="idx_employee_name"),
            models.Index(fields=["job_title"], name="idx_employee_job_title"),
            models.Index(fields=["country", "job_title"], name="idx_employee_country_job_title"),
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class EmployeeAudit(models.Model):
    """
    Audit model for employee salary changes.
    """
    employee = models.ForeignKey(to=Employee, on_delete=models.PROTECT, related_name="audits")
    old_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text="Old Salary of the employee in USD",
    )
    new_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        help_text="New Salary of the employee in USD",
    )
    note = models.TextField(blank=True, null=True, help_text="Note for the audit")