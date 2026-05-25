from django.db.models import Avg, Max, Min
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .aggregates import Median
from .models import Employee, EmploymentStatus, EmployeeAudit
from .serializers import EmployeeSerializer


class EmployeeViewSet(ModelViewSet):
    """CRUD operations for Employee records, plus salary insights by country, department, and job title."""

    queryset = Employee.objects.all().order_by("date_of_joining")
    serializer_class = EmployeeSerializer

    def perform_destroy(self, instance):
        """Soft-delete: marks the employee Inactive instead of removing the row."""
        instance.employment_status = EmploymentStatus.INACTIVE
        instance.save()

    @action(detail=False, methods=["get"])
    def insights(self, request):
        """Return min/max/avg/median salary grouped by country, department, and job title."""
        qs = Employee.objects.filter(employment_status=EmploymentStatus.ACTIVE)

        def salary_stats(group_field):
            return list(
                qs.values(group_field)
                .annotate(
                    min_salary=Min("salary"),
                    max_salary=Max("salary"),
                    avg_salary=Avg("salary"),
                    median_salary=Median("salary"),
                )
                .order_by(group_field)
            )

        return Response(
            {
                "by_country": salary_stats("country"),
                "by_department": salary_stats("department"),
                "by_title": salary_stats("job_title"),
            }
        )

    def update(self, request, *args, **kwargs):
        employee = self.get_object()
        old_salary = employee.salary
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        new_salary = serializer.validated_data.get("salary")
        if new_salary and new_salary != old_salary:
            employee_audit = EmployeeAudit.objects.create(
                employee=instance,
                old_salary=old_salary,
                new_salary=new_salary,
            )
            employee_audit.save()
        self.perform_update(serializer)
        return Response(serializer.data)
