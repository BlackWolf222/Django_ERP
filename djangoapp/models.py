from django.db import models
import uuid
from django.core.validators import EmailValidator

# Create your models here.

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    description = models.TextField(null=True, blank=True)
    employee_count = models.PositiveIntegerField(default=0, editable=False)

    def udate_count(self):
        self.employee_count = self.employees.count()
        self.save()

    def __str__(self):
        return self.name

class Employee(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator(message="Adj meg egy érvényes email címet!")])
    job_title = models.CharField(max_length=10, choices=[('developer', 'Developer'), ('designer', 'Designer'), ('manager', 'Manager'), ('tester', 'Tester')])
    age = models.PositiveIntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.company.udate_count()

    def delete(self, *args, **kwargs):
        company = self.company
        super().delete(*args, **kwargs)
        company.udate_count()
    
    def __str__(self):
        return f"{self.name} ({self.job_title})"