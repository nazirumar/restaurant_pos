from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem
from inventory.models import InventoryItem
from menu.models import MenuItemIngredient

@receiver(post_save, sender=OrderItem)
def update_inventory(sender, instance, created, **kwargs):
    if created and instance.order.status == 'preparing':
        for ing in MenuItemIngredient.objects.filter(menu_item=instance.menu_item):
            inv = InventoryItem.objects.get(ingredient=ing.ingredient)
            inv.stock_level -= ing.quantity * instance.quantity
            inv.save()