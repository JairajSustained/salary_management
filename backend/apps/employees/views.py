from django.db.models import Avg, Max, Min
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .aggregates import Median
from .models import Employee, EmploymentStatus
from .serializers import EmployeeSerializer


class EmployeeViewSet(ModelViewSet):
	queryset = Employee.objects.all().order_by("date_of_joining")
	serializer_class = EmployeeSerializer

	def perform_destroy(self, instance):
		instance.employment_status = EmploymentStatus.INACTIVE
		instance.save()

	@action(detail=False, methods=["get"])
	def insights(self, request):
		qs = Employee.objects.filter(employment_status=EmploymentStatus.ACTIVE)

		def salary_stats(group_field):
			return list(
				qs.values(group_field).annotate(
					min_salary=Min("salary"),
					max_salary=Max("salary"),
					avg_salary=Avg("salary"),
					median_salary=Median("salary"),
				).order_by(group_field)
			)

		return Response({
			"by_country": salary_stats("country"),
			"by_department": salary_stats("department"),
			"by_title": salary_stats("job_title"),
		})
