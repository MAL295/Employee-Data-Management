from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.db.models import Avg, Count
import csv,logging
from .models import Employee, PerformanceRecord, Attendance, DepartmentalPerformance
from .serializers import EmployeeSerializer, PerformanceRecordSerializer, AttendanceSerializer, DepartmentalPerformanceSerializer

logger = logging.getLogger(__name__)

class EmployeeViewSet(viewsets.ModelViewSet):
    # ...
    def create(self, request, *args, **kwargs):
        logger.info(f"Creating employee with data: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating employee: {e}")
            raise

class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class to set page size.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing employees.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'job_title']
    ordering_fields = ['first_name', 'last_name', 'hire_date', 'salary']
    pagination_class = CustomPageNumberPagination
    authentication_classes = [TokenAuthentication, BasicAuthentication] #  authentication
    permission_classes = [IsAuthenticated, DjangoModelPermissions] #  permissions
    throttle_classes = [UserRateThrottle] # Throttling
    
    @action(detail=False, methods=['get'])
    def health(self, request):
        """
        Endpoint to check the health of the API.
        """
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """
        Endpoint to export employee data to CSV.
        """
        employees = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(employees, many=True)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employees.csv"'
        
        writer = csv.writer(response)
        # Write header
        writer.writerow(serializer.data[0].keys())
        # Write data rows
        for row in serializer.data:
            writer.writerow(row.values())
        
        return response

class PerformanceRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing performance records.
    """
    queryset = PerformanceRecord.objects.all()
    serializer_class = PerformanceRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'review_date']
    ordering_fields = ['review_date', 'rating']
    pagination_class = CustomPageNumberPagination
    authentication_classes = [TokenAuthentication, BasicAuthentication] #  authentication
    permission_classes = [IsAuthenticated, DjangoModelPermissions] #  permissions
    throttle_classes = [UserRateThrottle] # Throttling

class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing employee attendance.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'date']
    ordering_fields = ['date', 'clock_in']
    pagination_class = CustomPageNumberPagination
    authentication_classes = [TokenAuthentication, BasicAuthentication]  # authentication
    permission_classes = [IsAuthenticated, DjangoModelPermissions]  # permissions
    throttle_classes = [UserRateThrottle]  # Throttling

class DepartmentalPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing departmental performance.
    """
    queryset = DepartmentalPerformance.objects.all()
    serializer_class = DepartmentalPerformanceSerializer
    authentication_classes = [TokenAuthentication, BasicAuthentication]  # authentication
    permission_classes = [IsAuthenticated]  # permissions
    throttle_classes = [UserRateThrottle, AnonRateThrottle]  # Throttling.  Added AnonRateThrottle
