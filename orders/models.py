from django.db import models
from tenants.models import Tenant
from menu.models import MenuItem
from users.models import User
from django.urls import reverse

class Table(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    number = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('tenant', 'number')

    def __str__(self):
        return f"{self.number} - {self.tenant.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('served', 'Served'),
        ('paid', 'Paid'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    waiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='waited_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        indexes = [models.Index(fields=['tenant', 'status', 'created_at'])]

    
    def __str__(self):
        return f"{self.status} - {self.tenant.name}"

    
    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

    
    # in Order model

    def update_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total = total
        self.save(update_fields=['total'])



    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Snapshot of price at order time



    def save(self, *args, **kwargs):
        if self.price is None and self.menu_item is not None:
            self.price = self.menu_item.price  # Take snapshot of price
        super().save(*args, **kwargs)
        self.update_order_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.update_total()

    def update_order_total(self):
        self.order.update_total()

    @property
    def subtotal(self):
        return self.quantity * self.price