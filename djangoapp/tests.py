from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Company, Employee

class CompanyViewSetTestCase(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company", address="123 Test St", phone="1234567890")
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            job_title="Developer",
            age=30,
            company=self.company
        )
        self.company_list_url = reverse('company-list')
        self.company_detail_url = reverse('company-detail', args=[self.company.id])

    def test_list_companies(self):
        response = self.client.get(self.company_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_companies_with_employees(self):
        response = self.client.get(self.company_list_url, {'with_employees': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('employees', response.data[0])

    def test_retrieve_company(self):
        response = self.client.get(self.company_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_company_with_employees(self):
        data = {
                "name": "New Company",
                "address": "456 New St",
                "phone": "9876543210",
                "employees": [
                    {
                        "name": "Jane Doe",
                        "email": "jane.doe@example.com",
                        "job_title": "manager",
                        "age": 35
                    }
                ]
        }
        response = self.client.post(self.company_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.filter(name="Jane Doe").exists())

    def test_destroy_company_with_employees(self):
        response = self.client.delete(self.company_detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy_company_without_employees(self):
        self.employee.delete()
        response = self.client.delete(self.company_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EmployeeViewSetTestCase(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company", address="123 Test St", phone="1234567890")
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            job_title="Developer",
            age=30,
            company=self.company
        )
        self.employee_list_url = reverse('employee-list')
        self.employee_detail_url = reverse('employee-detail', args=[self.employee.id])

    def test_list_employees(self):
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_employee(self):
        response = self.client.get(self.employee_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        data = {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "job_title": "tester",
            "age": 28,
            "company": self.company.id
        }
        response = self.client.post(self.employee_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.filter(name="Jane Smith").exists())

    def test_bulk_create_employees(self):
        url = reverse('employee-bulk')
        data = [
            {
                "name": "Emp1",
                "email": "emp1@example.com",
                "job_title": "developer",
                "age": 25,
                "company": self.company.id
            },
            {
                "name": "Emp2",
                "email": "emp2@example.com",
                "job_title": "developer",
                "age": 26,
                "company": self.company.id
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)

    def test_bulk_delete_employees(self):
        url = reverse('employee-bulk')
        data = [{"id": self.employee.id}]
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())