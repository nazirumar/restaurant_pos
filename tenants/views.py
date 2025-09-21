from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Tenant
from .forms import TenantForm
from users.models import User
import logging

logger = logging.getLogger(__name__)

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class TenantListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Tenant
    template_name = 'tenants/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant and not self.request.user.is_superuser:
            context['error'] = "No tenant associated with this request."
        return context

class TenantCreateView(LoginRequiredMixin, CreateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'tenants/create.html'
    success_url = reverse_lazy('tenant_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Assign the creator as a user with 'owner' role for this tenant
        user = self.request.user
        if not user.is_superuser:  # Superusers don't need tenant assignment
            user.tenant = form.instance
            user.role = 'owner'
            user.save()
            logger.debug(f"Assigned user {user.username} as owner of tenant {form.instance}")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant and not self.request.user.is_superuser:
            context['error'] = "No tenant associated with this request."
        return context

class TenantDetailView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    model = Tenant
    template_name = 'tenants/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant and not self.request.user.is_superuser:
            context['error'] = "No tenant associated with this request."
        return context

class TenantUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'tenants/update.html'
    success_url = reverse_lazy('tenant_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant and not self.request.user.is_superuser:
            context['error'] = "No tenant associated with this request."
        return context

class TenantDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Tenant
    template_name = 'tenants/delete.html'
    success_url = reverse_lazy('tenant_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant and not self.request.user.is_superuser:
            context['error'] = "No tenant associated with this request."
        return context