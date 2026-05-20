import datetime
import random
from django.db import transaction
from pathlib import Path

from django.core.management.base import BaseCommand

from apps.employees.models import Employee

from .constants import COUNTRIES, DEPARTMENT_ROLES

_DATA_DIR = Path(__file__).parent / "data"

_COUNT = 10_000
_BATCH_SIZE = 5_000


class Command(BaseCommand):
	"""Seed the database with 10,000 realistic employee records."""

	help = "Seed the database with 10,000 employees."

	def handle(self, *args, **options):
		first_names = (_DATA_DIR / "first_names.txt").read_text().splitlines()
		last_names = (_DATA_DIR / "last_names.txt").read_text().splitlines()

		# Pre-generate all random values at once using C-level random.choices
		dept_role_pairs = [
			(dept, role)
			for dept, roles in DEPARTMENT_ROLES.items()
			for role in roles
		]
		selected_pairs = random.choices(dept_role_pairs, k=_COUNT)
		first = random.choices(first_names, k=_COUNT)
		last = random.choices(last_names, k=_COUNT)
		countries = random.choices(COUNTRIES, k=_COUNT)
		salaries = random.choices(range(30_000, 200_001), k=_COUNT)

		start_date = datetime.date(2015, 1, 1)
		total_days = (datetime.date.today() - start_date).days
		day_offsets = random.choices(range(total_days + 1), k=_COUNT)

		employees = [
			Employee(
				first_name=first[i],
				last_name=last[i],
				department=selected_pairs[i][0],
				job_title=selected_pairs[i][1],
				country=countries[i],
				salary=salaries[i],
				date_of_joining=start_date + datetime.timedelta(days=day_offsets[i]),
			)
			for i in range(_COUNT)
		]
		with transaction.atomic():
			Employee.objects.bulk_create(employees, batch_size=_BATCH_SIZE, ignore_conflicts=True)
		self.stdout.write(self.style.SUCCESS("Successfully seeded 10,000 employees."))
