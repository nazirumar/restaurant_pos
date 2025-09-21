from django.db import models
from tenants.models import Tenant
from users.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='employees')
    phone = models.CharField(max_length=20, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, choices=[
        ('waiter', 'Waiter'),
        ('chef', 'Chef'),
        ('manager', 'Manager'),
        ('owner', 'Owner'),
    ])

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=['employee', 'start_time'])]