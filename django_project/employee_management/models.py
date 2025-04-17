from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Employee(models.Model):
    """
    Represents an employee in the company.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        # Add a unique constraint
        unique_together = ('email',)

class PerformanceRecord(models.Model):
    """
    Stores performance reviews for employees.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_records')
    review_date = models.DateField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )  # Rating from 1 to 5
    comments = models.TextField()
    reviewer_name = models.CharField(max_length=200)

    def __str__(self):
        return f"Performance Review for {self.employee} on {self.review_date}"
    
    class Meta:
        ordering = ['-review_date']  # Default ordering by review date

class Attendance(models.Model):
    """
    Records daily attendance for employees.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    clock_in = models.TimeField()
    clock_out = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee} - {self.date}"
    
    class Meta:
        unique_together = ('employee', 'date') # Ensure only one entry per employee per day

class DepartmentalPerformance(models.Model):
    """
    Tracks overall performance of departments.  Useful for analytics.
    """
    department_name = models.CharField(max_length=100, unique=True)
    average_rating = models.FloatField(default=0.0)  #  Average performance rating
    total_employees = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name
    
    class Meta:
        ordering = ['-average_rating']
