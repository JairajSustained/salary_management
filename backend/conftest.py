import datetime

import pytest

from apps.employees.models import Employee


@pytest.fixture
def employee_data():
	return {
		"first_name": "John",
		"last_name": "Doe",
		"job_title": "Software Engineer",
		"department": "Engineering",
		"country": "India",
		"salary": 50000.00,
		"status": "Active",
		"doj": datetime.datetime.now(),
	}


@pytest.fixture
def employee(employee_data):
	return Employee.objects.create(**employee_data)
