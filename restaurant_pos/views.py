from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order
from inventory.models import InventoryItem
from django.db.models import Sum
from django.db import models

from datetime import date

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.tenant:
            context['orders'] = Order.objects.filter(
                tenant=self.request.tenant, status='pending'
            ).select_related('table').prefetch_related('items')
            context['inventory_items'] = InventoryItem.objects.filter(
                tenant=self.request.tenant, stock_level__lt=models.F('low_stock_threshold')
            ).select_related('ingredient')
            today = date.today()
            sales = Order.objects.filter(
                tenant=self.request.tenant, status='paid', created_at__date=today
            ).aggregate(total=Sum('total'))
            context['today_sales'] = sales['total'] or 0
        else:
            context['orders'] = []
            context['inventory_items'] = []
            context['today_sales'] = 0
            context['error'] = "No tenant associated with this request."
        return context

def custom_404(request, exception):
    return HttpResponse('404 Not Found', status=404)

def custom_500(request):
    return HttpResponse('500 Server Error', status=500)