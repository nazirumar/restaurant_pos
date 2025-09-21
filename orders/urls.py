from django.urls import path
from .views import OrderCreateView, OrderListView, OrderDetailView, OrderUpdateView

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
]