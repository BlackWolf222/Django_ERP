from django_filters import rest_framework as filters
from .models import Employee, Company

class EmployeeFilter(filters.FilterSet):
    job_title = filters.CharFilter(lookup_expr='icontains', label='Job Title')
    company_name = filters.CharFilter(field_name='company__name', lookup_expr='icontains', label='Company Name')
    email = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['email','job_title', 'company_name']

class CompanyFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label='Company Name')
    employee_count = filters.NumberFilter(field_name='employee_count', lookup_expr='gte', label='Employee Count')
    address = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Company
        fields = ['name','address','employee_count']