

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
