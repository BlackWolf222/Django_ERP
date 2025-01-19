from rest_framework import serializers
from .models import Company, Employee
from rest_framework.validators import UniqueValidator
from django.core.validators import EmailValidator


class CompanySerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ['id','name','address','phone','description','employee_count']
        read_only_fields = ['id','employee_count']

class CompanyNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255,
        validators=[UniqueValidator(queryset=Employee.objects.all()), 
                    EmailValidator(message="Please provide a valid email address.")]
    )

    class Meta:
        model = Employee
        fields = ['id','name','email','job_title','age','company']
        read_only_fields = ['id']

    def validate(self, data):
        
        if not data.get('company'):
            raise serializers.ValidationError({'company': 'Company is required.'})
        
        if data['age'] < 18:
            raise serializers.ValidationError({"age": "Employees must be at least 18 years old."})
        
        return data

class EmployeeSerializerForBulk(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields = ['id','name','email','job_title','age','company']
        read_only_fields = ['id']

class EmployeeSerializerWithNest(serializers.ModelSerializer):
    
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'job_title', 'age', 'company']
        read_only_fields = ['id']

    def create(self, validated_data):
        
        return Employee.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        company = validated_data.pop('company', None)
        if company and company != instance.company:
            instance.company = company

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        
        representation = super().to_representation(instance)
        
        if instance.company:
            representation['company'] = CompanyNestedSerializer(instance.company).data
        
        return representation