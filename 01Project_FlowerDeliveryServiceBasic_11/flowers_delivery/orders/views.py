from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Order, Flower
from django.conf import settings
import requests
import os

from dotenv import load_dotenv
load_dotenv()
TELEGRAM_CHAT_ID = os.getenv('TG_CHAT_ID')
TELEGRAM_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')

def send_telegram_message(chat_id, message, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    return response.json()

@login_required
def create_order(request, flower_id):
    flower = Flower.objects.get(id=flower_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        recipient_name = request.POST['recipient_name']
        address = request.POST['address']
        phone = request.POST['phone']
        order = Order(user=request.user, flower=flower, quantity=quantity, recipient_name=recipient_name,
            address=address, phone=phone)

        order.save()

        # Отправка сообщения в Telegram
        chat_id = TELEGRAM_CHAT_ID
        bot_token = TELEGRAM_BOT_TOKEN
        message = f"Новый заказ!\nПользователь: {request.user.username}\nЗаказ: {flower.name}\nКоличество: {quantity}\nИмя получателя: {recipient_name}\nАдрес: {address}\nТелефон: {phone}"
        send_telegram_message(chat_id, message, bot_token)

        return redirect(reverse('order_success'))  # Перенаправление на страницу успеха

    return render(request, 'orders/create_order.html', {'flower': flower})


def order_success(request):
    return render(request, 'orders/order_success.html')
