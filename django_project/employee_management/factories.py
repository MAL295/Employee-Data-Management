import factory
import factory.fuzzy
from employee_management.models import Employee, PerformanceRecord, Attendance
from django.utils import timezone
import random

class EmployeeFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Employee instances.
    """
    class Meta:
        model = Employee

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    job_title = factory.Faker('job')
    department = factory.Faker('word')  # Keep it simple, or use a list of departments
    hire_date = factory.Faker('date_between', start_date='-10y', end_date='-1y')
    salary = factory.FuzzyInteger(50000, 150000)
    is_active = True

class PerformanceRecordFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating PerformanceRecord instances.
    """
    class Meta:
        model = PerformanceRecord

    employee = factory.SubFactory(EmployeeFactory)  # Use SubFactory
    review_date = factory.Faker(
        'date_between',
        start_date=factory.SelfAttribute('employee.hire_date'),  # Corrected attribute access
        end_date='today'
    )
    rating = factory.FuzzyInteger(1, 5)
    comments = factory.Faker('text')
    reviewer_name = factory.Faker('name')

class AttendanceFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Attendance instances.
    """
    class Meta:
        model = Attendance

    employee = factory.SubFactory(EmployeeFactory)
    date = factory.Faker('date_between', start_date='-1y', end_date='today')
    clock_in = factory.Faker('time')
    clock_out = factory.Faker('time')  #  simplified
    notes = factory.Faker('text')
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default _create method."""
        employee = kwargs.pop('employee')
        date = kwargs.pop('date')
        
        # Ensure that an attendance record for the same employee and date does not already exist
        try:
            return model_class.objects.get(employee=employee, date=date)
        except model_class.DoesNotExist:
            return super()._create(model_class, *args, **kwargs)
