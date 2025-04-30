from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, OrderForm
from .models import Product, Order
from .telegram_bot import send_order_notification
from django.contrib.auth.models import User
import logging


def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Перенаправление на страницу входа после регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/register.html', {'form': form})


@login_required
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            form.save_m2m()  # Сохраняем связь с продуктами
            send_order_notification(order)  # Отправляем уведомление в Teleg
            return redirect('home')  # Перенаправляем на главную страницу после оформления заказа
        else:
            logging.warning("Форма заказа не прошла валидацию: %s", form.errors)
    else:
        form = OrderForm()
    return render(request, 'shop/order.html', {'form': form})