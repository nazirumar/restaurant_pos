from django import forms
from .models import InventoryItem

class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['stock_level']