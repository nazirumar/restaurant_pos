from django.db import models
from tenants.models import Tenant
from django.core.validators import MinValueValidator
from menu.models import Ingredient

class Supplier(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE)
    stock_level = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    low_stock_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    class Meta:
        indexes = [models.Index(fields=['tenant', 'stock_level'])]

    @property
    def is_low_stock(self):
        if self.stock_level is None or self.low_stock_threshold is None:
            return False  # or True, depending on your use case
        return self.stock_level < self.low_stock_threshold
    
    def __str__(self):
        return f"{self.ingredient.name} - {self.tenant.name}"