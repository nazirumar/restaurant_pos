from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order
from .forms import OrderForm
from django.db.models import Prefetch

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/list.html'

    def get_queryset(self):
        if self.request.tenant:
            return Order.objects.filter(tenant=self.request.tenant).select_related('table', 'waiter').prefetch_related('items')
        return Order.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/create.html'

    

    def form_valid(self, form):
        if not self.request.tenant:
            form.add_error(None, "No tenant associated with this request.")
            return self.form_invalid(form)
        form.instance.tenant = self.request.tenant
        form.instance.waiter = self.request.user
        return super().form_valid(form)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/update.html'

    def get_queryset(self):
        if self.request.tenant:
            return Order.objects.filter(tenant=self.request.tenant)
        return Order.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class KitchenQueueView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'placeholder.html'

    def get_queryset(self):
        return Order.objects.filter(tenant=self.request.tenant, status='pending').prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('menu_item'))
        )