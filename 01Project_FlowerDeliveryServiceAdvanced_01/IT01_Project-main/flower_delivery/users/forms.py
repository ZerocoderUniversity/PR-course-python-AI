from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, PasswordInput

class CustomUserCreationForm(UserCreationForm):
       class Meta:
           model = User
           fields = ['username', 'email', 'password1', 'password2']
           widgets = {'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя', 'label': 'Имя пользователя'}),
                      'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите E-mail', 'label': 'Введите E-mail'}),
                      'password1': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль', 'label': 'Пароль'}),
                      'password2': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль', 'label': 'Подтвердите пароль'})
                     }
class CustomAuthenticationForm(AuthenticationForm):
       class Meta:
           model = User
           fields = ['username', 'password']
           widgets = {'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя', 'label': 'Имя пользователя'}),
                      'password': PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
                     }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя', 'label': 'Имя'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия', 'label': 'Фамилия'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите адрес', 'rows': 3}),
        }