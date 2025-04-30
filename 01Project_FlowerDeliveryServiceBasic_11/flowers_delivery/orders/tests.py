# Тесты для models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Flower
from .models import Order

class OrderModelTests(TestCase):

    def setUp(self):
        # Создание пользователя для тестов
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )

        # Создание товара для тестов
        self.flower = Flower.objects.create(
            name='Rose',
            price=10.99,
            description='Red Rose'
        )

    def test_create_order(self):
        # Создание заказа
        order = Order.objects.create(
            user=self.user,
            flower=self.flower,
            quantity=5,
            recipient_name='John Doe',
            address='123 Main St',
            phone='1234567890'
        )

        # Проверка, что заказ был создан
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.flower, self.flower)
        self.assertEqual(order.quantity, 5)
        self.assertEqual(order.recipient_name, 'John Doe')
        self.assertEqual(order.address, '123 Main St')
        self.assertEqual(order.phone, '1234567890')

    def test_order_default_values(self):
        # Создание заказа с использованием значений по умолчанию
        order = Order.objects.create(
            user=self.user,
            flower=self.flower,
            quantity=3
        )

        # Проверка значений по умолчанию
        self.assertEqual(order.recipient_name, 'Получатель не указан')
        self.assertEqual(order.address, 'Адрес не указан')
        self.assertEqual(order.phone, 'Телефон не указан')

    def test_order_str_method(self):
        # Создание заказа
        order = Order.objects.create(
            user=self.user,
            flower=self.flower,
            quantity=2,
            recipient_name='Jane Doe',
            address='456 Elm St',
            phone='0987654321'
        )

        # Проверка метода __str__
        expected_str = f"Заказ #{order.id} от {self.user} для Jane Doe"
        self.assertEqual(str(order), expected_str)


# Тесты для forms.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Flower
from .models import Order
from .forms import OrderForm

class OrderFormTests(TestCase):

    def setUp(self):
        # Создание пользователя для тестов
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com'
        )

        # Создание товара для тестов
        self.flower = Flower.objects.create(
            name='Rose',
            price=10.99,
            description='Red Rose'
        )

    def test_order_form_valid(self):
        # Данные для создания формы
        form_data = {
            'flower': self.flower.id,
            'quantity': 5
        }

        # Создание формы с валидными данными
        form = OrderForm(data=form_data)

        # Проверка, что форма валидна
        self.assertTrue(form.is_valid())

        # Сохранение формы и проверка, что объект был создан
        order = form.save(commit=False)
        order.user = self.user  # Устанавливаем пользователя
        order.save()
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.flower, self.flower)
        self.assertEqual(order.quantity, 5)

    def test_order_form_invalid(self):
        # Данные для создания формы с некорректным количеством
        form_data = {
            'flower': self.flower.id,
            'quantity': -1  # Некорректное количество
        }

        # Создание формы с невалидными данными
        form = OrderForm(data=form_data)

        # Проверка, что форма невалидна
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_order_form_required_fields(self):
        # Данные без указания обязательного поля 'quantity'
        form_data = {
            'flower': self.flower.id
        }

        # Создание формы с невалидными данными
        form = OrderForm(data=form_data)

        # Проверка, что форма невалидна
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)


# Тесты для views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from .models import Flower, Order
from .views import send_telegram_message


class OrderViewTests(TestCase):

    def setUp(self):
        # Создание пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Создание цветка
        self.flower = Flower.objects.create(name='Rose', price=10.00, description='Beautiful red rose')
        self.client.login(username='testuser', password='testpassword')

    def test_create_order_get(self):
        response = self.client.get(reverse('create_order', args=[self.flower.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/create_order.html')

    @patch('requests.post')
    def test_create_order_post(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {'ok': True})

        response = self.client.post(reverse('create_order', args=[self.flower.id]), {
            'quantity': 1,
            'recipient_name': 'John Doe',
            'address': '123 Main St',
            'phone': '1234567890'
        })

        # Проверяем, что заказ был создан
        self.assertEqual(Order.objects.count(), 1)

        # Проверяем редирект
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('order_success'))

        # Проверяем, что сообщение было отправлено в Telegram
        self.assertTrue(mock_post.called)

        payload = mock_post.call_args[1]['data']
        self.assertIn('chat_id', payload)
        self.assertIn('text', payload)
        self.assertIn('bot{bot_token}', mock_post.call_args[0][0])

    def test_order_success_view(self):
        response = self.client.get(reverse('order_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_success.html')


class SendTelegramMessageTests(TestCase):

    @patch('requests.post')
    def test_send_telegram_message(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {'ok': True})

        chat_id = 'test_chat_id'
        message = 'Test message'
        bot_token = 'test_bot_token'

        response = send_telegram_message(chat_id, message, bot_token)

        self.assertTrue(mock_post.called)
        self.assertEqual(response['ok'], True)

        payload = mock_post.call_args[1]['data']
        self.assertEqual(payload['chat_id'], chat_id)
        self.assertEqual(payload['text'], message)
        self.assertEqual(payload['parse_mode'], 'HTML')


# Тесты для urls.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import create_order, order_success

class UrlsTestCase(SimpleTestCase):

    def test_create_order_url(self):
        # Проверяем, что URL-адрес для создания заказа правильно разрешается
        url = reverse('create_order', args=[1])
        self.assertEqual(url, '/create/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, create_order)

    def test_order_success_url(self):
        # Проверяем, что URL-адрес для страницы успеха заказа правильно разрешается
        url = reverse('order_success')
        self.assertEqual(url, '/order_success/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, order_success)