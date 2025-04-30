import telebot

# Инициализация бота с использованием вашего токена
TOKEN = '7601500603:AAHa4m39mM9_3t0ktBFk373WGwK0xPufZu8'
bot = telebot.TeleBot(TOKEN)

# Фиксированный chat_id для отправки сообщений
CHAT_ID = '1019653173'


def send_order_notification(order_data):
    message = (
        f"Новый заказ!\n"
        f"ID заказа: {order_data['order_id']}\n"
        f"Имя клиента: {order_data['customer_name']}\n"
        f"Общая стоимость: {order_data['total_price']} руб.\n"
    )
    bot.send_message(CHAT_ID, message)