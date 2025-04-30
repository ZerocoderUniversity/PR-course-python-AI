from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from catalog.models import Product
from account.models import User

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        comment = request.POST.get('comment')

        # Обновляем номер телефона, если он был изменен
        if phone_number and phone_number != request.user.phone_number:
            request.user.phone_number = phone_number
            request.user.save()

        if first_name and first_name != request.user.first_name:
            request.user.first_name = first_name
            request.user.save()

        if last_name and last_name != request.user.last_name:
            request.user.last_name = last_name
            request.user.save()

        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            product=product,
            address=address,
            user_comment=comment,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )

        return redirect('orders:order_success')  # Перенаправляем на страницу подтверждения или успеха

    return render(request, 'orders/create_orders.html', {'product': product, 'user': request.user})

@login_required
def repeat_order(request, order_id):
    original_order = get_object_or_404(Order, id=order_id, user=request.user)
    # Создаем новый заказ на основе оригинального
    new_order = Order.objects.create(
        user=original_order.user,
        first_name=original_order.first_name,
        last_name=original_order.last_name,
        product=original_order.product,
        address=original_order.address,
        user_comment=original_order.user_comment,
        phone_number=original_order.phone_number,
    )
    return redirect('account:profile')  # Перенаправляем пользователя обратно в профиль

def order_success(request):
    return render(request, 'orders/order_success.html')