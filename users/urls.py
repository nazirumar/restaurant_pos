from django.urls import path
from .views import CustomLoginView,CustomLogoutView,RegistrationView

urlpatterns = [
    path('signup', RegistrationView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
 
]