from django import forms
from .models import User, Order, OrderItem, Product


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Отображение пароля в виде скрытого поля

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1})
        }


class OrderForm(forms.ModelForm):
    items = forms.inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True)

    class Meta:
        model = Order
        fields = ['user', 'status']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all()
        self.fields['status'].choices = Order.STATUS_CHOICES
