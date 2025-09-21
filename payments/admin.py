from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'tenant', 'amount', 'method', 'transaction_id', 'paid_at')
    list_filter = ('tenant', 'method', 'paid_at')
    search_fields = ('order__id', 'transaction_id')
    ordering = ('-paid_at',)
    autocomplete_fields = ('tenant', 'order')
    readonly_fields = ('paid_at',)
