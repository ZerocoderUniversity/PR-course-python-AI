from django import forms
from .models import Order, Flower2, Select_shop

class ADD_TO_ORDER_FORM(forms.Form):
    select = forms.ModelChoiceField(queryset=Flower2.objects.all())

    class Meta:
        model = Order
        fields = ['select']

class ShoppingForm(forms.ModelForm):

    class Meta:
        model = Select_shop
        fields = ['products']