from django.urls import path
from .views import TenantListView, TenantCreateView, TenantDetailView, TenantUpdateView, TenantDeleteView

urlpatterns = [
    path('', TenantListView.as_view(), name='tenant_list'),
    path('create/', TenantCreateView.as_view(), name='tenant_create'),
    path('<int:pk>/', TenantDetailView.as_view(), name='tenant_detail'),
    path('<int:pk>/update/', TenantUpdateView.as_view(), name='tenant_update'),
    path('<int:pk>/delete/', TenantDeleteView.as_view(), name='tenant_delete'),
]