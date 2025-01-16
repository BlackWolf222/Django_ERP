from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer

# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=True, methods=['get'])
    def employees(self, regquest, pk=None):
        company = self.get_object()
        employees = Employee.objects.filter(company=company)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

class EmployeeViewSet(viewsets.ModelViewSet):
    
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class CompanyEmployeeListView(generics.ListAPIView):

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return Employee.objects.filter(company_id=company_id)