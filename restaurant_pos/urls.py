from django.contrib import admin
from django.urls import path, include
from .views import DashboardView, custom_404, custom_500

handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('tenants/', include('tenants.urls')),
    path('users/', include('users.urls')),
    path('menu/', include('menu.urls')),
    path('inventory/', include('inventory.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('employees/', include('employees.urls')),
    path('reports/', include('reports.urls')),
]