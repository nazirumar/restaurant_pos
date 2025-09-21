from django.urls import path
from .views import InventoryListView, InventoryUpdateView, LowStockAlertView

urlpatterns = [
    path('', InventoryListView.as_view(), name='inventory_list'),
    path('<int:pk>/update/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('low-stock/', LowStockAlertView.as_view(), name='low_stock'),
]