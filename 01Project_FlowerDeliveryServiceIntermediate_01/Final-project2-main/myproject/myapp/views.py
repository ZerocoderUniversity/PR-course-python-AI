from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import Profile, Product, Basket, BasketItem, Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .bot import send_order_to_telegram  # Импортируем функцию отправки в Telegram

def get_cart_item_count(request):
    # Пример логики для подсчета количества товаров в корзине
    basket, created = Basket.objects.get_or_create(user=request.user)
    return sum(item.quantity for item in basket.items.all())

def index(request):
    return render(request, 'layoute.html')

def home(request):
    products = Product.objects.all()  # Получить все продукты из базы данных
    cart_item_count = get_cart_item_count(request)  # Получить количество товаров в корзине
    context = {
        'products': products,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'home.html', context)

@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket, created = Basket.objects.get_or_create(user=request.user)
    basket_item, item_created = BasketItem.objects.get_or_create(basket=basket, product=product)

    if not item_created:
        basket_item.quantity += 1
        basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def basket(request):
    basket, created = Basket.objects.get_or_create(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in basket.items.all())
    orders = Order.objects.filter(user=request.user).exclude(status='completed')

    return render(request, 'basket.html', {'basket': basket, 'total_price': total_price, 'orders': orders})

@login_required
def remove_from_basket(request, item_id):
    basket_item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
    basket_item.delete()
    return redirect('basket')


@login_required
def checkout(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        address = request.POST.get('address')
        date = request.POST.get('date')
        time = request.POST.get('time')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment')

        basket, created = Basket.objects.get_or_create(user=request.user)

        if not basket.items.exists():
            message = "Корзина пуста!"
            return render(request, 'basket.html', {'basket': basket, 'total_price': 0, 'message': message})

        order = Order.objects.create(
            user=request.user,
            city=city,
            address=address,
            date=date,
            time=time,
            phone=phone,
            comment=comment
        )

        for item in basket.items.all():
            basket_item_copy = BasketItem.objects.create(
                basket=None,
                product=item.product,
                quantity=item.quantity
            )
            order.items.add(basket_item_copy)

        send_order_to_telegram(order)

        basket.items.all().delete()

        message = 'Ваш заказ успешно оформлен! Перейдите в раздел "История заказов" чтобы увидеть!'
        return render(request, 'basket.html', {'basket': basket, 'total_price': 0, 'message': message})

    return redirect('basket')

def story_view(request):
    orders = Order.objects.filter(user=request.user).exclude(status='completed')
    return render(request, 'story.html', {'orders': orders})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Измените 'layoute' на 'home'
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('layoute')

def layoute(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile = Profile.objects.get(user=request.user)
    return render(request, 'layoute.html', {'profile': profile})