from django.test import TestCase
from .models import Order

class OrderModelTest(TestCase):
def setUpTestData(cls):
    Order.objects.create(
    order_number='12345',
    customer_name='John Doe',
    total_amount=99.99
    )

def test_order_creation(self):
    order = Order.objects.get(order_number='12345')
    self.assertEqual(order.customer_name, 'John Doe')
    self.assertEqual(order.total_amount, 99.99)

def test_order_str_method(self):
    order = Order.objects.get(order_number='12345')
    self.assertEqual(str(order), 'Order 12345 for John Doe')

def test_order_update(self):
    order = Order.objects.get(order_number='12345')
    order.customer_name = 'Jane Doe'
    order.save()
    self.assertEqual(order.customer_name, 'Jane Doe')

def test_order_delete(self):
    order = Order.objects.get(order_number='12345')
    order.delete()
    orders_count = Order.objects.count()
    self.assertEqual(orders_count, 0)