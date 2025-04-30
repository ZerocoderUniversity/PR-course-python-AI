import sqlite3
import telebot
import time
import logging
from config import TELEGRAM_BOT_TOKEN, TG_CHAT_ID

# Параметры
DB_PATH = 'db.sqlite3'  # Укажите реальный путь
TELEGRAM_TOKEN = TELEGRAM_BOT_TOKEN
CHAT_ID = TG_CHAT_ID
CHECK_INTERVAL = 30  # Интервал проверки в секундах

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def fetch_new_orders():
    """
    Возвращает новые заказы из базы данных.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            query = """
            SELECT orders_order.id, orders_order.address, orders_order.user_comment,
                   catalog_product.name AS product_name, catalog_product.price,
                   account_user.first_name, account_user.last_name, account_user.phone_number
            FROM orders_order
            JOIN catalog_product ON orders_order.product_id = catalog_product.id
            JOIN account_user ON orders_order.user_id = account_user.id
            WHERE orders_order.status = 'new'
            """
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")
        return []

def update_order_status(order_id):
    """
    Обновляет статус заказа в базе данных на 'notified'.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE orders_order SET status = 'notified' WHERE id = ?", (order_id,))
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Не удалось обновить статус заказа {order_id}: {e}")

def send_order_notification(order):
    """
    Отправляет уведомление о новом заказе в Telegram.
    """
    order_id, address, comment, product_name, price, first_name, last_name, phone_number = order
    message = (
        f"📦 *Новый заказ* #{order_id}\n\n"
        f"👤 Покупатель: {first_name} {last_name}\n"
        f"📞 Телефон: {phone_number}\n"
        f"🏡 Адрес: {address}\n"
        f"📌 Комментарий: {comment or 'Нет'}\n\n"
        f"🎁 Товар: {product_name}\n"
        f"💰 Цена: {price} ₽"
    )
    try:
        bot.send_message(CHAT_ID, message, parse_mode='Markdown')
        logging.info(f"Уведомление отправлено для заказа #{order_id}")
    except Exception as e:
        logging.error(f"Ошибка отправки уведомления для заказа #{order_id}: {e}")

def start_bot():
    """
    Основной цикл проверки базы данных и отправки уведомлений.
    """
    logging.info("Бот запущен!")
    while True:
        orders = fetch_new_orders()
        for order in orders:
            send_order_notification(order)
            update_order_status(order[0])
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    start_bot()
