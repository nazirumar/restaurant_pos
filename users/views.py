from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from .models import User

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Placeholder

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class RegistrationView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signUp.html'

