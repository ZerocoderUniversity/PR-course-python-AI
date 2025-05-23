from django.test import TestCase
from .models import Order
from django.contrib.auth import get_user_model
from catalog.models import Product
from manage_orders.models import ManageOrder

class OrderTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            image='test_image.jpg'
        )

    def test_order_is_created(self):
        order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            product=self.product,
            address='Test Address',
            phone_number='1234567890',
            status='new'
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.first_name, 'Test')
        self.assertEqual(order.last_name, 'User')
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.address, 'Test Address')
        self.assertEqual(order.phone_number, '1234567890')
        self.assertEqual(order.status, 'new')

    def test_manage_order_is_created(self):
        order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            product=self.product,
            address='Test Address',
            phone_number='1234567890',
            status='new'
        )
        manage_order = ManageOrder.objects.get(order_id=order.id)
        self.assertEqual(manage_order.order_id, order)
        self.assertEqual(manage_order.phone_number, order.phone_number)
        self.assertEqual(manage_order.first_name, order.first_name)
        self.assertEqual(manage_order.last_name, order.last_name)
        self.assertEqual(manage_order.user_comment, order.user_comment)

#Этот тест проверяет создание заказа и создание соответствующего объекта ManageOrder
    def test_orders_by_user(self):

        Order.objects.create(
            user=self.user,
            first_name='Test2',
            last_name='User2',
            product=self.product,
            address='Test Address2',
            phone_number='1234567891',
            status='notified'
        )
        orders = Order.objects.filter(user=self.user)
        self.assertEqual(orders.count(), 2)