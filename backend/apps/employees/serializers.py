from .models import Employee
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee model
    """

    class Meta:
        model = Employee
        fields = "__all__"
