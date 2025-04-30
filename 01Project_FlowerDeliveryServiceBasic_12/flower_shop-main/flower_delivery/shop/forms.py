from django import forms
from django.contrib.auth.models import User
from .models import Order

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class OrderForm(forms.ModelForm):
    delivery_address = forms.CharField(max_length=255, required=True, label='Адрес доставки')
    delivery_date = forms.DateField(required=True, label='Дата доставки')
    delivery_time = forms.TimeField(required=True, label='Время доставки')
    comments = forms.CharField(widget=forms.Textarea, required=False, label='Комментарий')

    class Meta:
        model = Order
        fields = ['products', 'delivery_address', 'delivery_date', 'delivery_time', 'comments']