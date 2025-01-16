from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Prefetch
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer

# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    def retrieve(self, request, *args, **kwargs):
        company = self.get_object()

        with_employees = request.query_params.get('with_employees', '0') == '1'
        
        serializer = self.get_serializer(company)
        response_data = serializer.data
        
        if with_employees:
            employees = Employee.objects.filter(company=company)
            employee_serializer = EmployeeSerializer(employees, many=True)
            response_data['employees'] = employee_serializer.data

        return Response(response_data)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class CompanyEmployeeListView(generics.ListAPIView):

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return Employee.objects.filter(company_id=company_id)