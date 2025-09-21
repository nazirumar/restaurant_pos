from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Tenant(TenantMixin):
    name = models.CharField(max_length=100, unique=True)
    subdomain = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)  # 👈 add thi
    created_at = models.DateTimeField(auto_now_add=True)

    auto_create_schema = True

    class Meta:
        indexes = [models.Index(fields=['subdomain'])]


    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass