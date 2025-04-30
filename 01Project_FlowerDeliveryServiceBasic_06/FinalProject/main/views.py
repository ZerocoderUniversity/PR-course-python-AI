from django.shortcuts import render, redirect
from .forms import UserForm
from .models import *
from .forms import OrderForm
from django.shortcuts import render, redirect
from .forms import OrderForm, OrderItemForm
from .models import OrderItem
from .bot import send_order_notification

def index(request):
    return render(request, 'main/index.html', {'caption': 'Доставка цветов'})

def new(request):
    return render(request, 'main/new.html')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UserForm()
    return render(request, 'main/register.html', {'form': form})

def success(request):
    return render(request, 'main/success.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'main/product_list.html', {'products': products})

from django.shortcuts import render

def order_success(request):
    return render(request, 'main/order_success.html')


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Сохраняем заказ и получаем объект
            order = form.save()

            # Данные для Telegram (упрощенные)
            order_data = {
                'order_id': order.id,
                'customer_name': order.user.username,
                'total_price': order.total_price,
            }

            # Попытка отправить сообщение в Telegram
            try:
                send_order_notification(order_data)
            except Exception as e:
                print("Ошибка при отправке сообщения:", e)

            return redirect('order_success')
    else:
        form = OrderForm()

    return render(request, 'main/place_order.html', {'form': form})


