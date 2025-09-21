from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Employee
from .forms import EmployeeForm
import logging

logger = logging.getLogger(__name__)

class ManagerOrOwnerRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        return self.request.user.is_authenticated and self.request.user.role in ['manager', 'owner']

class EmployeeListView(LoginRequiredMixin, ManagerOrOwnerRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/list.html'
    permission_required = 'employees.view_employee'

    def get_queryset(self):
        if self.request.tenant:
            return Employee.objects.filter(tenant=self.request.tenant).select_related('user')
        logger.warning("No tenant associated, returning empty queryset")
        return Employee.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class EmployeeCreateView(LoginRequiredMixin, ManagerOrOwnerRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/create.html'
    success_url = reverse_lazy('employee_list')
    permission_required = 'employees.add_employee'

    def form_valid(self, form):
        if not self.request.tenant:
            form.add_error(None, "No tenant associated with this request.")
            return self.form_invalid(form)
        form.instance.tenant = self.request.tenant
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class EmployeeDetailView(LoginRequiredMixin, ManagerOrOwnerRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/detail.html'
    permission_required = 'employees.view_employee'

    def get_queryset(self):
        if self.request.tenant:
            return Employee.objects.filter(tenant=self.request.tenant).select_related('user')
        return Employee.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class EmployeeUpdateView(LoginRequiredMixin, ManagerOrOwnerRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/update.html'
    success_url = reverse_lazy('employee_list')
    permission_required = 'employees.change_employee'

    def get_queryset(self):
        if self.request.tenant:
            return Employee.objects.filter(tenant=self.request.tenant).select_related('user')
        return Employee.objects.none()

    def form_valid(self, form):
        if not self.request.tenant:
            form.add_error(None, "No tenant associated with this request.")
            return self.form_invalid(form)
        form.instance.tenant = self.request.tenant
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class EmployeeDeleteView(LoginRequiredMixin, ManagerOrOwnerRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/delete.html'
    success_url = reverse_lazy('employee_list')
    permission_required = 'employees.delete_employee'

    def get_queryset(self):
        if self.request.tenant:
            return Employee.objects.filter(tenant=self.request.tenant)
        return Employee.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context