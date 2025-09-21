from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import SalesReport
from orders.models import Order
from django.db.models import Sum
from django.db import models
from datetime import date

class ReportGenerateView(LoginRequiredMixin, ListView):
    model = SalesReport
    template_name = 'placeholder.html'

    def get_queryset(self):
        tenant = self.request.tenant
        today = date.today()
        sales = Order.objects.filter(tenant=tenant, status='paid', created_at__date=today).aggregate(total=Sum('total'), count=models.Count('id'))
        report, created = SalesReport.objects.get_or_create(tenant=tenant, date=today, defaults={'total_sales': sales['total'] or 0, 'orders_count': sales['count'] or 0})
        return SalesReport.objects.filter(tenant=tenant)

def export_csv(request):
    # Placeholder for CSV export
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'
    # Write data...
    return response