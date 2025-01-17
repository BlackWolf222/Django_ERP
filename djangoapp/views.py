from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.decorators import action
from django.db.models import Prefetch
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer

# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get','put','post','patch','delete']
    
    def partial_update(self, request, *args, **kwargs):
        """
        Overriding partial_update to restrict fields that can be updated with PATCH.
        """
        allowed_fields = {'phone', 'description'}
        incoming_fields = set(request.data.keys())
        # Validate that incoming fields are allowed
        if not incoming_fields.issubset(allowed_fields):
            raise PermissionDenied(
                f"You can only update the fields: {', '.join(allowed_fields)}."
            )
        # Proceed with the normal partial_update process
        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Overrides the default list method to handle the `with_employees` query parameter.
        """
        with_employees = request.query_params.get('with_employees', '0')  # Default is 0 (don't include employees)

        if with_employees == '1':
            # Include employees
            companies = self.get_queryset()
            data = []
            for company in companies:
                company_data = CompanySerializer(company).data
                employees = Employee.objects.filter(company=company)
                employee_data = EmployeeSerializer(employees, many=True).data
                company_data['employees'] = employee_data
                data.append(company_data)
            return Response(data)

        # Default behavior (without employees)
        return super().list(request, *args, **kwargs)

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
    
    def create(self, request, *args, **kwargs):
        """
        POST: Create a new company, optionally including employees.
        Supports adding employees by their data (via 'employees') or their IDs (via 'employee_ids').
        """
        # Extract optional employee data
        employee_data = request.data.pop('employees', [])
        employee_ids = request.data.pop('employee_ids', [])

        company_serializer = self.get_serializer(data=request.data)
        if company_serializer.is_valid():
            company = company_serializer.save()

            # Create new employees if provided
            if employee_data:
                for employee in employee_data:
                    employee['company'] = company.id
                employee_serializer = EmployeeSerializer(data=employee_data, many=True)
                if employee_serializer.is_valid():
                    employee_serializer.save()
                else:
                    return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Associate existing employees by their IDs
            if employee_ids:
                employees = Employee.objects.filter(id__in=employee_ids)
                if employees.count() != len(employee_ids):
                    return Response(
                        {"error": "One or more employee IDs are invalid."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                employees.update(company=company)

            return Response(company_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):

        if request.method == 'PUT':
            return Response({"details": "PUT is not allowed for companies"}, status=status.HTTP_405_METHOD_NOT_ALLOWED) #error message mby

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        company = self.get_object()

        if Employee.objects.filter(company=company).exists():
            raise ValidationError("Company cannot be deleted as it has associated employees.")
        return super().destroy(request, *args, **kwargs)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get','put','post','patch','delete']