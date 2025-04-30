from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Product, Order, OrderItem  # Импортируем модели
from .forms import OrderCreateForm  # Импортируем форму создания заказа
from .bots.notify_shop import notify_shop  # Импортируем уведомление для Telegram

import logging

# Настройка логирования
logger = logging.getLogger(__name__)

@login_required
# Отображение списка товаровa
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


# Представление корзины
def cart(request):
    cart = request.session.get('cart', {})  # Получаем корзину из сессии

    cart_items = []
    total_price = 0
    for item_id, item_data in cart.items():
        product = get_object_or_404(Product, id=item_id)
        quantity = item_data['quantity']
        total_item_price = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_item_price})
        total_price += total_item_price

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # По умолчанию количество 1

        cart = request.session.get('cart', {})

        # Получаем продукт из базы данных
        product = get_object_or_404(Product, id=product_id)

        # Если продукт уже в корзине, обновляем количество, иначе добавляем товар
        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            # Убедитесь, что цена сохраняется в корзину
            cart[product_id] = {'quantity': quantity, 'price': float(product.price)}  # Преобразуем Decimal в float

        # Сохраняем корзину в сессии
        request.session['cart'] = cart
        return redirect('cart')

    return redirect('product_list')


@login_required
def order_create(request):
    cart = request.session.get('cart', {})  # Получаем корзину из сессии
    if not cart:
        return redirect('product_list')  # Если корзина пуста, перенаправляем на каталог

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart.values())
            order.save()

            # Добавляем товары в заказ
            for item_id, item_data in cart.items():
                product = Product.objects.get(id=item_id)
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item_data['price'],
                    quantity=item_data['quantity']
                )
                order_item.save()

            # Очищаем корзину
            request.session['cart'] = {}

            # Уведомляем администратора о новом заказе
            notify_shop(order)

            return redirect('order_history')
    else:
        form = OrderCreateForm()

    return render(request, 'shop/order_create.html', {'form': form, 'cart': cart})

@login_required
def order_history(request):
    """
    Показывает историю заказов пользователя.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})

