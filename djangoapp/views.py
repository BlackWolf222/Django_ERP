from rest_framework import viewsets, generics,  status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EmployeeFilter, CompanyFilter
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer, EmployeeSerializerWithNest, EmployeeSerializerForBulk

# Create your views here.

class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get','put','post','patch','delete']
    pagination_class = Pagination
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    filterset_class = CompanyFilter
    search_fields = ['name', 'address', 'phone','id']

    ordering_fields = ['name', 'address','phone','employee_count']
    ordering = ['employee_count'] 

    def list(self, request, *args, **kwargs):
        with_employees = request.query_params.get('with_employees', '0')

        if with_employees == '1':
            companies = self.get_queryset()
            data = []
            for company in companies:
                company_data = CompanySerializer(company).data
                employees = Employee.objects.filter(company=company)
                employee_data = EmployeeSerializer(employees, many=True).data
                company_data['employees'] = employee_data
                data.append(company_data)
            return Response(data)

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
        data = request.data.copy()
        
        employee_data = data.pop('employees', [])
        employee_ids = data.pop('employee_ids', [])

        company_serializer = self.get_serializer(data=data)
        if company_serializer.is_valid():
            company = company_serializer.save()

            if employee_data:
                for employee in employee_data:
                    employee['company'] = company.id
                employee_serializer = EmployeeSerializer(data=employee_data, many=True)
                if employee_serializer.is_valid():
                    employee_serializer.save()
                else:
                    return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"details": "PUT is not allowed for companies"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        company = self.get_object()

        if Employee.objects.filter(company=company).exists():
            raise ValidationError("Company cannot be deleted as it has associated employees.")

        return super().destroy(request, *args, **kwargs)


class CompanyEmployeeListView(generics.ListAPIView):
    http_method_names = ['get','put','post','patch','delete']
    serializer_class = EmployeeSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    filterset_class = CompanyFilter
    search_fields = ['name', 'address', 'phone','id']

    ordering_fields = ['name', 'address','phone','employee_count']
    ordering = ['employee_count']

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return Employee.objects.filter(company_id=company_id)


class EmployeeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get','put','post','patch','delete']
    queryset = Employee.objects.select_related('company')
    serializer_class = EmployeeSerializerWithNest
    pagination_class = Pagination
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    filterset_class = EmployeeFilter
    search_fields = ['name', 'email', 'job_title','id','company'] 
    
    
    ordering_fields = ['name', 'email', 'job_title','age']
    ordering = ['name']
    
    def get_serializer_class(self):
        
        if self.action == 'bulk':
            return EmployeeSerializerForBulk
        return EmployeeSerializerWithNest
    
    @action(detail=False, methods=["post", "put", "patch", "delete"])
    def bulk(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({"detail": "Payload must be a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

        method = request.method.upper()

        if method == "POST":
            
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif method in ["PUT", "PATCH"]:
            
            partial = method == "PATCH"
            updated_employees = []

            for item in request.data:
                employee_id = item.get("id")
                if not employee_id:
                    return Response({"detail": "Each object must contain an 'id' field."}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    instance = self.get_queryset().get(pk=employee_id)
                except Employee.DoesNotExist:
                    return Response({"detail": f"Employee with id {employee_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

                serializer = self.get_serializer(instance, data=item, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                updated_employees.append(serializer.data)

            return Response(updated_employees, status=status.HTTP_200_OK)

        elif method == "DELETE":
            
            ids = [item.get('id') for item in request.data]
            if not ids:
                return Response({"detail": "Payload must contain a list of objects with 'id' fields."}, status=status.HTTP_400_BAD_REQUEST)

            deleted_count, _ = self.get_queryset().filter(id__in=ids).delete()
            return Response({"detail": f"Deleted {deleted_count} employees."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Unsupported HTTP method for bulk operations."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)