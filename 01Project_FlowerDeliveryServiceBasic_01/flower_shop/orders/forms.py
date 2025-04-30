from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address']
        labels = {
            'delivery_address': 'Адрес доставки',
        }
