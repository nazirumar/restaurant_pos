from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from tenants.models import Tenant

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('waiter', 'Waiter'),
        ('kitchen_staff', 'Kitchen Staff'),
    ], default='waiter')

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions",
        related_query_name="user",
    )

    class Meta:
        unique_together = ('username', 'tenant')
        indexes = [models.Index(fields=['tenant', 'role'])]

    def __str__(self):
        return self.username



