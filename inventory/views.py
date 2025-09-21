from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InventoryItem
from .forms import InventoryUpdateForm
from django.db.models import F

class InventoryListView(LoginRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'inventory/list.html'

    def get_queryset(self):
        if self.request.tenant:
            return InventoryItem.objects.filter(tenant=self.request.tenant).select_related('ingredient', 'supplier')
        return InventoryItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryUpdateForm
    template_name = 'inventory/update.html'

    def get_queryset(self):
        if self.request.tenant:
            return InventoryItem.objects.filter(tenant=self.request.tenant)
        return InventoryItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class LowStockAlertView(LoginRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'inventory/low_stock.html'

    def get_queryset(self):
        if self.request.tenant:
            return InventoryItem.objects.filter(tenant=self.request.tenant, stock_level__lt=F('low_stock_threshold')).select_related('ingredient', 'supplier')
        return InventoryItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context