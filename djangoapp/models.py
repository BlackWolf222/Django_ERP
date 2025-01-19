from django.db import models
import uuid

# Create your models here.

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    description = models.TextField(null=True, blank=True)
    employee_count = models.PositiveIntegerField(default=0, editable=False)

    def update_count(self):
        self.employee_count = self.employees.count()
        self.save()

    def __str__(self):
        return self.name

class Employee(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    job_title = models.CharField(max_length=10, choices=[('developer', 'Developer'), ('designer', 'Designer'), ('manager', 'Manager'), ('tester', 'Tester')])
    age = models.PositiveIntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")

    def save(self, *args, **kwargs): 
        old_company_id = None

        if self.pk:
            old_company_id = Employee.objects.filter(pk=self.pk).values_list('company_id', flat=True).first()

        super().save(*args, **kwargs)

        if old_company_id and old_company_id != self.company_id:
            old_company = Company.objects.filter(id=old_company_id).first()
            if old_company:
                old_company.update_count()

        self.company.update_count()

        self.company.update_count()

    def delete(self, *args, **kwargs):
        company = self.company
        super().delete(*args, **kwargs)
        company.update_count()
    
    def __str__(self):
        return f"{self.name} ({self.job_title})"