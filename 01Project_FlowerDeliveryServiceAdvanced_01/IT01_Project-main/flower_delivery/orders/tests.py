from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cart, CartItem, Order
from flowers.models import Flowers
from .forms import OrderForm

class CartViewsTests(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')


        self.flower = Flowers.objects.create(title="Роза", short_description="Красный", price=1000, on_sale=True,
                               image='static/flowers/img/cat/rose1.jpg')

        self.cart = Cart.objects.create()
        self.client.session['cart_id'] = self.cart.id

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.flower.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().flowers, self.flower)

    def test_cart_view(self):
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/cart.html')

    #def test_order_create(self):
        # response = self.client.post(reverse('order_create'), {
        #     'customer_name': 'testuser',
        #     'phone': '123 Test St',
        #     'email': 'Test City',
        #     'address': '12345',
        #     'cart': self.cart
        # })
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(Order.objects.count(), 1)

    def test_order_success_view(self):
        response = self.client.get(reverse('order_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_success.html')

    def test_update_cart_item(self):
        cart_item = CartItem.objects.create(cart=self.cart, flowers=self.flower, quantity=1)
        response = self.client.post(reverse('update_cart_item'), {
            'cart_id': self.cart.id,
            f'cart_item_id_{cart_item.id}': cart_item.id,
            f'quantity_{cart_item.id}': '2'
        })
        self.assertEqual(response.status_code, 302)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 2)

    def test_orders_view(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders.html')

    def test_order_view(self):
        order = Order.objects.create(cart=self.cart, user=self.user)
        response = self.client.get(reverse('order_view', args=[order.id]))
        self.assertEqual(response.status_code, 200)  # Проверяем статус
        self.assertTemplateUsed(response, 'orders/order_view.html')

    def test_order_repeat(self):
        order = Order.objects.create(cart=self.cart, user=self.user)
        response = self.client.get(reverse('order_repeat', args=[order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cart.objects.count(), 2)

    def test_order_denied_view(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpass')
        order = Order.objects.create(cart=self.cart, user=another_user)
        response = self.client.get(reverse('order_view', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_denied.html')