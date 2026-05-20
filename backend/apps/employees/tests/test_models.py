import pytest
import uuid

@pytest.mark.django_db
class TestEmployeeModel:
	def test_employee_can_be_created(self, employee):
		assert employee.id is not None

	def test_employee_id_is_uuid(self,employee):
		assert isinstance(employee.id, uuid.UUID)

	def test_employee_full_name(self, employee):
		assert employee.first_name == "John"
		assert employee.last_name == "Doe"
		assert employee.full_name == "John Doe"

	def test_employee_default_status_is_active(self, employee):
		assert employee.employment_status == "Active"

	def test_employee_salary_is_stored_correctly(self, employee):
		assert employee.salary == 5 * 10**5