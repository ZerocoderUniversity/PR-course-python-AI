
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from .models import User

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=12,
        help_text='Введите корректный номер телефона до 11 цифр.',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'})
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number:
            raise forms.ValidationError('Пожалуйста, введите номер телефона')
        if not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        return phone_number

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=''
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')

        def clean_username(self):
            username = self.cleaned_data['username']
            if not username:
                raise forms.ValidationError('Пожалуйста, введите логин')
            if len(username) > 150:
                raise forms.ValidationError('Логин не может быть более 150 символов')
            if not username.isalnum() and not any(char in username for char in '@/./+/-/_'):
                raise forms.ValidationError('Логин может содержать только буквы, цифры и символы @/./+/-/_')
            return username

        def clean_phone_number(self):
            phone_number = self.cleaned_data['phone_number']
            if not phone_number:
                raise forms.ValidationError('Пожалуйста, введите номер телефона')
            if not phone_number.isdigit():
                raise forms.ValidationError('Номер телефона должен состоять только из цифр')
            return phone_number

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'