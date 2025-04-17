from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, PerformanceRecordViewSet, AttendanceViewSet, DepartmentalPerformanceViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'performance-records', PerformanceRecordViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'department-performance', DepartmentalPerformanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]