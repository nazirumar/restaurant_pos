from django import forms
from .models import Employee
from users.models import User
from django.contrib.auth.forms import UserCreationForm

class EmployeeForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    }))
    hire_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
        'type': 'date'
    }))
    role = forms.ChoiceField(choices=Employee._meta.get_field('role').choices, widget=forms.Select(attrs={
        'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'hire_date', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            employee = Employee.objects.create(
                user=user,
                tenant=self.instance.tenant,  # Set in view
                phone=self.cleaned_data['phone'],
                hire_date=self.cleaned_data['hire_date'],
                role=self.cleaned_data['role']
            )
            user.role = self.cleaned_data['role']  # Sync role with User
            user.save()
        return user