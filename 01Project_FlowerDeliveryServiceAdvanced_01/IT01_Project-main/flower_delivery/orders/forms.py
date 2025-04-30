from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'email', 'address']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Ваше имя','label': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Ваш телефон','label': 'Ваш телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите Ваш Email','label': 'Ваш Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите Ваш адрес', 'rows': 3,'label': 'Адрес доставки'}),
        }