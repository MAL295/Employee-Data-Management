from django.core.management.base import BaseCommand
from faker import Faker
from employee_management.models import Employee, PerformanceRecord, Attendance, DepartmentalPerformance
from django.utils import timezone
import random
from django.db import transaction

class Command(BaseCommand):
    """
    Command to generate synthetic employee data.
    """
    help = 'Generates synthetic employee data'

    def handle(self, *args, **options):
        """
        Handles the execution of the command.
        """
        fake = Faker()

        # Use a transaction to improve performance.
        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS("Deleting existing data..."))
            # Delete all existing data
            Employee.objects.all().delete()
            PerformanceRecord.objects.all().delete()
            Attendance.objects.all().delete()
            DepartmentalPerformance.objects.all().delete()

            self.stdout.write(self.style.SUCCESS("Creating departments..."))
            # Create Departments
            departments = ['Sales', 'Marketing', 'Engineering', 'HR', 'Finance']
            for dept_name in departments:
                DepartmentalPerformance.objects.create(department_name=dept_name)

            self.stdout.write(self.style.SUCCESS("Creating employees..."))
            # Create employees
            employees = []
            for _ in range(5):  # Generate 5 employees
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()
                job_title = fake.job()
                department = random.choice(departments)
                hire_date = fake.date_between(start_date='-10y', end_date='-1y')
                salary = fake.random_int(min=50000, max=150000)
                is_active = fake.boolean()
                
                employee = Employee(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    job_title=job_title,
                    department=department,
                    hire_date=hire_date,
                    salary=salary,
                    is_active=is_active,
                )
                employees.append(employee)
            
            Employee.objects.bulk_create(employees) # Use bulk_create

            # Get all employees
            employees = Employee.objects.all() # get the employees from DB

            self.stdout.write(self.style.SUCCESS("Creating performance records..."))
            # Create performance records
            for employee in employees:
                for _ in range(3):  # Each employee has 3 performance records
                    review_date = fake.date_between(start_date=employee.hire_date, end_date='today')
                    rating = fake.random_int(min=1, max=5)
                    comments = fake.text()
                    reviewer_name = fake.name()
                    PerformanceRecord.objects.create(
                        employee=employee,
                        review_date=review_date,
                        rating=rating,
                        comments=comments,
                        reviewer_name=reviewer_name,
                    )
            
            self.stdout.write(self.style.SUCCESS("Creating attendance records..."))
            # Create attendance records
            for employee in employees:
                for _ in range(20):  # 20 attendance records per employee
                    date = fake.date_between(start_date='-1y', end_date='today')
                    clock_in = fake.time()
                    clock_out = fake.time() if fake.boolean(chance_of_getting_true=70) else None  # 70% chance of clocking out
                    notes = fake.text() if fake.boolean(chance_of_getting_true=20) else None
                    Attendance.objects.create(
                        employee=employee,
                        date=date,
                        clock_in=clock_in,
                        clock_out=clock_out,
                        notes=notes,
                    )
            
            self.stdout.write(self.style.SUCCESS("Updating Departmental Performance"))
            # Update Departmental Performance
            for dept_name in departments:
                department = DepartmentalPerformance.objects.get(department_name=dept_name)
# Calculate the average rating for the department.
                avg_rating = PerformanceRecord.objects.filter(employee__department=dept_name).aggregate(Avg('rating'))['rating__avg']
                employee_count = Employee.objects.filter(department=dept_name).count()
                
                department.average_rating = avg_rating if avg_rating else 0.0
                department.total_employees = employee_count
                department.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated synthetic data.'))