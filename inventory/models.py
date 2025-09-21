from django.db import models
from tenants.models import Tenant
from django.core.validators import MinValueValidator
from menu.models import Ingredient

class Supplier(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=255, blank=True)

class InventoryItem(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE)
    stock_level = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    low_stock_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    class Meta:
        indexes = [models.Index(fields=['tenant', 'stock_level'])]

    def is_low_stock(self):
        return self.stock_level < self.low_stock_threshold