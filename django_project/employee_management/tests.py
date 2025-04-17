from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Employee, PerformanceRecord, Attendance
from .factories import EmployeeFactory, PerformanceRecordFactory, AttendanceFactory  # If you use factory_boy

class EmployeeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee1 = EmployeeFactory()
        self.employee2 = EmployeeFactory()

    def test_get_employee_list(self):
        url = reverse('employee-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_employee_detail(self):
        url = reverse('employee-detail', kwargs={'pk': self.employee1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.employee1.email)

    # Add more tests for create, update, delete, filter, etc.

class PerformanceRecordAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.record1 = PerformanceRecordFactory()
        self.record2 = PerformanceRecordFactory()

    def test_get_performance_record_list(self):
        url = reverse('performancerecord-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Add more tests

class AttendanceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.attendance1 = AttendanceFactory()
        self.attendance2 = AttendanceFactory()

    def test_get_attendance_list(self):
        url = reverse('attendance-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)