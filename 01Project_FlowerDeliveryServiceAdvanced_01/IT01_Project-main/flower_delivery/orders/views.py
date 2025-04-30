from django.shortcuts import render, redirect,get_object_or_404
from .models import Cart, CartItem, Order
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth.models import User
from flowers.models import Flowers
from .forms import OrderForm
from django.http import JsonResponse

def add_to_cart(request, flowers_id):
    flowers = Flowers.objects.get(id=flowers_id)
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id', None))
    cart_item, created = CartItem.objects.get_or_create(cart=cart, flowers=flowers)
    cart_item.quantity += 1
    cart_item.save()
    request.session['cart_id'] = cart.id
    return redirect('catalog')



def cart_view(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart = None
    else:
        cart = Cart.objects.get(id=request.session.get('cart_id'))
    return render(request, 'orders/cart.html', {'cart': cart})


def order_create(request):
    print(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.cart = Cart.objects.get(id=request.session.get('cart_id'))
            if request.user.is_authenticated:
                order.user = request.user
            else:
                username = request.POST.get('username', 'guest_' + str(request.session.session_key))
                password = request.POST.get('password', 'defaultpassword')
                email = request.POST.get('email', '')

                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                login(request, user)
                order.user = user

            order.save()
            del request.session['cart_id']  # Очистка корзины
            return redirect('order_success')
    else:
        if request.user.is_authenticated:
            form = OrderForm(initial={'customer_name': request.user.first_name, 'email': request.user.email, 'phone': request.user.profile.phone_number,'address': request.user.profile.address})
        else:
            form = OrderForm()
    return render(request, 'orders/order.html', {'form': form, 'cart': Cart.objects.get(id=request.session.get('cart_id'))})


def order_success(request):
    print(request)
    return render(request, 'orders/order_success.html')


@require_POST
def update_cart_item(request):
    cart_id = request.POST.get('cart_id')
    # Получаем корзину по cart_id
    cart = get_object_or_404(Cart, id=cart_id)
    # Получаем все CartItem из корзины
    cart_items_list = list(CartItem.objects.filter(cart=cart))
    for cart_item in cart_items_list:
        cart_item_id = cart_item.id
        key_index = f'quantity_{cart_item_id}'
        new_quantity = request.POST.get(key_index)
        if new_quantity.isdigit() and int(new_quantity) > 0:
            cart_item.quantity = int(new_quantity)
            cart_item.save()  # Сохраняем изменения
        else:
            cart_item.delete()  # Удаляем CartItem

    return redirect('cart_view')

def orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'orders/orders.html', {'orders': orders})

def order_view(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id)
    if order.user != user:
        return render(request, 'orders/order_denied.html')
    return render(request, 'orders/order_view.html', {'order': order})

def order_repeat(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id)
    cart_old = order.cart
    cart_items = cart_old.cartitem_set.all()
    cart = Cart.objects.create()
    for cart_item in cart_items:
        cart_item_new = CartItem.objects.create(cart=cart, flowers=cart_item.flowers, quantity=cart_item.quantity)
        cart_item_new.save()
    cart.save()
    request.session['cart_id'] = cart.id
    if order.user != user:
        return render(request, 'orders/order_denied.html')
    #return render(request, 'order_create', {'cart': cart})
    return redirect('order_create')