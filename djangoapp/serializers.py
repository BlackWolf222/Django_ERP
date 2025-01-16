from rest_framework import serializers
from .models import Company, Employee

class CompanySerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ['id','name','address','phone','description','employee_count']
        read_only_fields = ['id','employee_count']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id']

    #delete mby
    def validate(self, data):
        """Custom validation to ensure company exists when creating an employee."""
        if not data.get('company'):
            raise serializers.ValidationError({'company': 'Company is required.'})
        return data