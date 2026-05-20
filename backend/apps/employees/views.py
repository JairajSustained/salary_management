from rest_framework.viewsets import ModelViewSet

from .models import Employee, EmploymentStatus
from .serializers import EmployeeSerializer


class EmployeeViewSet(ModelViewSet):
	queryset = Employee.objects.all().order_by("date_of_joining")
	serializer_class = EmployeeSerializer

	def perform_destroy(self, instance):
		instance.employment_status = EmploymentStatus.INACTIVE
		instance.save()
