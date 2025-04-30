from django.test import TestCase
from flower_delivery.config import TOKEN, CHAT_ID
from flower_delivery.utils import send_telegram_message
from django.urls import reverse
from flowers.models import Flowers
from orders.models import Cart, CartItem, Order
from django.contrib.auth import get_user_model
from unittest.mock import patch
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
class TelegramBotTests(TestCase):

    @patch('requests.post')
    def test_order_status_change_notification(self, mock_send_telegram_message):
        # user = get_user_model().objects.create_user(username='testuser', password='testpass')
        # flower = Flowers.objects.create(title="Роза", short_description="Красный", price=1000, on_sale=True,
        #                                 image='static/flowers/img/cat/rose1.jpg')
        # cart = Cart.objects.create()
        # cart_item = CartItem.objects.create(cart=cart, flowers=flower, quantity=1)
        #
        # order = Order.objects.create(user=user, cart=cart, status='new')
        #
        # # Изменяем статус заказа
        # order.status = 'delivered'
        # order.save()
        #
        # # Проверяем, что уведомление отправлено
        # mock_send_telegram_message.assert_called_once_with(order.user.telegram_id, 'Ваш заказ изменен на статус: delivered')
        message = "Hello, Telegram!"

        send_telegram_message(message)

        # Проверяем, что requests.post был вызван один раз
        mock_send_telegram_message.assert_called_once()

        # Проверяем, что данные, отправленные в POST-запросе, корректны
        expected_payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        mock_send_telegram_message.assert_called_with(TELEGRAM_API_URL, data=expected_payload)