from django.contrib import admin
from .models import Supplier, InventoryItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'contact')
    list_filter = ('tenant',)
    search_fields = ('name', 'contact')
    ordering = ('tenant', 'name')
    autocomplete_fields = ('tenant',)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'tenant', 'stock_level', 'low_stock_threshold', 'is_low_stock_display', 'supplier')
    list_filter = ('tenant', 'supplier')
    search_fields = ('ingredient__name',)
    ordering = ('tenant', 'ingredient__name')
    autocomplete_fields = ('tenant', 'ingredient', 'supplier')
    readonly_fields = ('is_low_stock_display',)

    def is_low_stock_display(self, obj):
        return obj.is_low_stock
    is_low_stock_display.boolean = True
    is_low_stock_display.short_description = 'Low Stock?'
