from django.db import models
from tenants.models import Tenant

class SalesReport(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    orders_count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('tenant', 'date')
        indexes = [models.Index(fields=['tenant', 'date'])]