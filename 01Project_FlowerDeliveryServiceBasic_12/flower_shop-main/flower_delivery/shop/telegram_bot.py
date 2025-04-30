import logging
import telebot
from flask import Flask, request

logging.basicConfig(level=logging.INFO)

# Укажите токен вашего бота
TELEGRAM_TOKEN = '7159096633:AAEUqc5-pwHXAHjz9MA_raXz_0-6mBe8PZQ'
CHAT_ID = '1072340585'


bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_order_notification(order):
    message = (
        f"Новый заказ!\n"
        f"Пользователь: {order.user.username}\n"
        f"Адрес доставки: {order.delivery_address}\n"
        f"Дата доставки: {order.delivery_date}\n"
        f"Время доставки: {order.delivery_time}\n"
        f"Комментарий: {order.comments}\n"
        f"Товары: {', '.join([product.name for product in order.products.all()])}\n"
    )
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        logging.info("Уведомление о заказе отправлено успешно.")
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")