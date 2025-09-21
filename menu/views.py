from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import MenuItem, Category, Allergen, Ingredient
from .forms import MenuItemForm

class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'menu/list.html'

    def get_queryset(self):
        if self.request.tenant:
            return MenuItem.objects.filter(tenant=self.request.tenant).select_related('category').prefetch_related('ingredients', 'allergens')
        return MenuItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class MenuItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/create.html'
    permission_required = 'menu.add_menuitem'

    def form_valid(self, form):
        if not self.request.tenant:
            form.add_error(None, "No tenant associated with this request.")
            return self.form_invalid(form)
        form.instance.tenant = self.request.tenant
        return super().form_valid(form)

class MenuItemDetailView(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = 'menu/detail.html'

    def get_queryset(self):
        if self.request.tenant:
            return MenuItem.objects.filter(tenant=self.request.tenant).select_related('category').prefetch_related('ingredients', 'allergens')
        return MenuItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class MenuItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/update.html'
    permission_required = 'menu.change_menuitem'

    def get_queryset(self):
        if self.request.tenant:
            return MenuItem.objects.filter(tenant=self.request.tenant)
        return MenuItem.objects.none()

    def form_valid(self, form):
        if not self.request.tenant:
            form.add_error(None, "No tenant associated with this request.")
            return self.form_invalid(form)
        form.instance.tenant = self.request.tenant
        return super().form_valid(form)

class MenuItemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'menu/delete.html'
    success_url = reverse_lazy('menu_list')
    permission_required = 'menu.delete_menuitem'

    def get_queryset(self):
        if self.request.tenant:
            return MenuItem.objects.filter(tenant=self.request.tenant)
        return MenuItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'menu/category_list.html'

    def get_queryset(self):
        if self.request.tenant:
            return Category.objects.filter(tenant=self.request.tenant)
        return Category.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class AllergenListView(LoginRequiredMixin, ListView):
    model = Allergen
    template_name = 'menu/allergen_list.html'

    def get_queryset(self):
        return Allergen.objects.all()  # Allergens are global, not tenant-specific

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context

class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'menu/ingredient_list.html'

    def get_queryset(self):
        if self.request.tenant:
            return Ingredient.objects.filter(tenant=self.request.tenant)
        return Ingredient.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.tenant:
            context['error'] = "No tenant associated with this request."
        return context