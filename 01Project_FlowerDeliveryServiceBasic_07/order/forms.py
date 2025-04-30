from django import forms
from .models import Order, OrderItem
from register.models import User
from catalog.models import Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'address']

class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']