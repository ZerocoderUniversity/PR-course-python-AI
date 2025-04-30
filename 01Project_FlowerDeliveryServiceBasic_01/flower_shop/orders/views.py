from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import OrderForm
from .models import Order
from products.models import Product
from telegram_bot.bot import send_order_notification

# Создание нового заказа
@login_required
def create_order(request):
    # Получение текущего времени
    current_time = now().time()

    # Устанавливаем границы рабочего времени
    start_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = current_time.replace(hour=23, minute=0, second=0, microsecond=0)

    if not (start_time <= current_time <= end_time):
        # Передача сообщения в шаблон
        return render(request, 'orders/create_order.html', {
            'error_message': 'Заказы можно оформлять только в рабочее время с 9:00 до 23:00.',
        })

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            order.products.set(Product.objects.filter(id__in=request.POST.getlist('products')))

            # Отправляем уведомление в Telegram
            send_order_notification(order.id)

            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()

    products = Product.objects.all()
    return render(request, 'orders/create_order.html', {'form': form, 'products': products})

# Подробности заказа
@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
