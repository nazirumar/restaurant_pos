from django.contrib import admin
from .models import Table, Order, OrderItem


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'tenant', 'capacity')
    list_filter = ('tenant',)
    search_fields = ('number',)
    ordering = ('tenant', 'number')
    autocomplete_fields = ('tenant',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ('menu_item',)
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'table', 'waiter', 'status', 'total', 'created_at')
    list_filter = ('tenant', 'status', 'created_at')
    search_fields = ('id', 'table__number', 'waiter__username')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    readonly_fields = ('total', 'created_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'price')
    list_filter = ('order__tenant',)
    search_fields = ('order__id', 'menu_item__name')
    autocomplete_fields = ('order', 'menu_item')
    readonly_fields = ('price',)
