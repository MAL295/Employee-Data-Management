import csv
from django.http import HttpResponse
from django.shortcuts import render # Added to remove import error
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def export_to_csv(queryset, filename, header=None):
    """
    Exports a Django queryset to a CSV file.

    Args:
        queryset: The Django queryset to export.
        filename: The name of the CSV file (without the .csv extension).
        header: (Optional) A list of field names for the CSV header.  If not
            provided, the function will use the fields from the first object
            in the queryset.
    Returns:
        A Django HttpResponse with the CSV data.
    """
    if not queryset:
        # Return a user-friendly message
        return HttpResponse("No data to export.", content_type="text/plain")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)
    
    if header:
        writer.writerow(header)
    else:
        # Use the fields from the model
        first_object = queryset.first()
        if not first_object:
            return HttpResponse("No data to export", content_type='text/plain')
        
        header = [field.name for field in first_object._meta.fields]
        writer.writerow(header)

    for obj in queryset:
        row = []
        for field_name in header:
            try:
                field_value = getattr(obj, field_name)
                if callable(field_value):
                    field_value = field_value()  # Handle callable attributes (e.g., methods)
                row.append(field_value)
            except AttributeError:
                row.append('')  # Handle fields that don't exist on this object
        writer.writerow(row)
    return response

@api_view(['GET'])
def export_employees_csv(request):
    """
    View to export all employees to a CSV file.
    """
    from employee_management.models import Employee  # Import here to avoid circular imports
    employees = Employee.objects.all()
    return export_to_csv(employees, 'employees')