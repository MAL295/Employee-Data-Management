from rest_framework import serializers
from .models import Employee, PerformanceRecord, Attendance, DepartmentalPerformance

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee model.
    """
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'job_title', 'department', 'hire_date', 'salary', 'is_active']
        #  Added unique together constraint in Model, no need here.
        # extra_kwargs = {'email': {'validators': []}} # removes the unique validator

class PerformanceRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for PerformanceRecord model.
    """
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all()) # changed to PK
    employee_name = serializers.CharField(source='employee', read_only=True) # added employee name
    class Meta:
        model = PerformanceRecord
        fields = ['id', 'employee', 'employee_name', 'review_date', 'rating', 'comments', 'reviewer_name']

class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Attendance model.
    """
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())  # Changed to PK
    employee_name = serializers.CharField(source='employee', read_only=True)
    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'employee_name', 'date', 'clock_in', 'clock_out', 'notes']
        #  Added unique together constraint in Model, no need here.
        # extra_kwargs = {
        #     'date': {'validators': []},
        #     'employee': {'validators': []}
        # }

class DepartmentalPerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for DepartmentalPerformance model
    """
    class Meta:
        model = DepartmentalPerformance
        fields = ['id', 'department_name', 'average_rating', 'total_employees', 'last_updated']