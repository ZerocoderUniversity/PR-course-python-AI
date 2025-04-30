from django import forms
from django.contrib.auth.models import User
from .models import Order

# Форма для создания заказа
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order  # Модель Order используется для формы
        fields = ['delivery_address']  # Поля, которые должны быть видимыми в форме

        # Кастомизация отображения полей формы
        widgets = {
            'delivery_address': forms.TextInput(attrs={
                'class': 'form-control',  # Используем Bootstrap-классы для стилизации
                'placeholder': 'Введите адрес доставки'
            }),
        }
        labels = {
            'delivery_address': 'Адрес доставки',
        }

# Форма регистрации пользователя (если она требуется в проекте)
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите пароль'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите email'
            }),
        }
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }

    # Дополнительная валидация для проверки совпадения паролей
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
