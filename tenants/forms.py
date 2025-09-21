from django import forms
from .models import Tenant

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'subdomain']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'subdomain': forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
        }

    def clean_subdomain(self):
        subdomain = self.cleaned_data['subdomain'].lower()
        if Tenant.objects.filter(subdomain=subdomain).exists():
            raise forms.ValidationError("This subdomain is already in use.")
        if not subdomain.isalnum():
            raise forms.ValidationError("Subdomain must contain only alphanumeric characters.")
        return subdomain