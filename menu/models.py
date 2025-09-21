from django.db import models
from tenants.models import Tenant
from django.core.validators import MinValueValidator

class Category(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('tenant', 'name')

    def __str__(self):
        return self.name

class Allergen(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    class Meta:
        unique_together = ('tenant', 'name')

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    ingredients = models.ManyToManyField(Ingredient, through='MenuItemIngredient')
    allergens = models.ManyToManyField(Allergen, blank=True)

    class Meta:
        unique_together = ('tenant', 'name')
        indexes = [models.Index(fields=['tenant', 'category'])]

    def __str__(self):
        return self.name

class MenuItemIngredient(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.menu_item.name