from django.contrib import admin
from .models import SalesReport


@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'date', 'total_sales', 'orders_count')
    list_filter = ('tenant', 'date')
    search_fields = ('tenant__name',)
    ordering = ('-date',)
    autocomplete_fields = ('tenant',)
    readonly_fields = ('total_sales', 'orders_count')
