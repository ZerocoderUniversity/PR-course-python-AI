from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Flower2, Order, Select_shop
from .forms import ADD_TO_ORDER_FORM, ShoppingForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import requests
from shop.tg_bot import API_TOKEN

# Create your views here.
def index(request):
    return render(request, 'shop/index.html')

def add_to_shopping(request):
    if request.method == 'POST':
        product_id = request.POST.get('flower_id')
        print(f"product_id = {product_id}")
        # Пытаемся получить объект продукта
        try:
            product = Flower2.objects.get(id=product_id)
            print("выполнил product = Flower2.objects.get")
        except Flower2.DoesNotExist:
            print("Продукт не найден")
            raise Http404("Продукт не найден")
        # Предположим, что у вас есть только одна корзина
        select_shop, created = Select_shop.objects.get_or_create(id=1)
        print("выполнил select_shop")
        # Добавляем продукт в корзину
        select_shop.products.add(product)
        print("выполнил добавление в корзину")
        return redirect('orders')

@login_required
def catalog(request):
    flowers = Flower2.objects.all()
    return render(request, 'shop/catalog.html', {'flowers': flowers})

@login_required
def orders(request):
    print("in orders")
    # Получаем существующую корзину или создаем новую
    select_shop, created = Select_shop.objects.get_or_create(id=1)
    # Получаем все продукты в корзине
    products = select_shop.products.all()
    # Передаем продукты в шаблон
    context = {
        'products': products
    }
    return render(request, 'shop/orders.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('catalog')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def clear_cart(request):
    # Получаем существующую корзину
    select_shop, created = Select_shop.objects.get_or_create(id=1)
    # Удаляем все продукты из корзины
    select_shop.products.clear()
    # Перенаправляем обратно на страницу заказа
    return redirect('orders')


@login_required
def place_order(request):
    # Получаем текущую корзину
    select_shop, created = Select_shop.objects.get_or_create(id=1)

    # Проверяем, есть ли продукты в корзине
    if select_shop.products.exists():
        # Создаем новый заказ
        order = Order.objects.create(user=request.user)
        # Добавляем продукты в заказ
        order.products.set(select_shop.products.all())
        # Очищаем корзину после оформления заказа
        select_shop.products.clear()

    # Перенаправляем на страницу заказов или подтверждения
    return redirect('my_orders')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('products')
    return render(request, 'shop/my_orders.html', {'orders': orders})

def delete_order(request, order_id):
    print("in delete_order")
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
        print(f"order = {order}")
        order.delete()
        print("deleted")
    return redirect('my_orders')  # Замените 'my_orders' на имя вашего пути для страницы заказов

@login_required
def send_orders_to_telegram(request):
    if request.method == "POST":
        user_orders = Order.objects.filter(user=request.user)
        message = "Ваши заказы:\n"
        for order in user_orders:
            products = ", ".join([product.name for product in order.products.all()])
            message += f"Заказ #{order.id}: {products}\n"

        # Отправляем сообщение в телеграмм бот
        telegram_api_url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
        data = {
            'chat_id': 960068824, #request.user.username,  # предполагается, что username в User - это ID пользователя в телеграмме
            'text': message
        }

        response = requests.post(telegram_api_url, data=data)
        if response.status_code == 200:
            # Сообщение успешно отправлено
            # Вы можете добавить сообщение об успехе, если хотите
            print("Сообщение успешно отправлено")
        else:
            # Ошибка при отправке сообщения
            # Вы можете добавить обработку ошибок здесь
            print("Ошибка при отправке сообщения")

    return redirect('my_orders')