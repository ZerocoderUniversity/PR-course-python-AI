# shop/bots/notify_shop.py

from django.conf import settings
from telegram import Bot
def notify_shop(order):
    """
    Отправляет уведомление в Telegram админу магазина о новом заказе.
    """
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    # Формируем сообщение с товарами в заказе
    order_items = order.orderitem_set.all()  # Получаем все товары в заказе через модель OrderItem
    items_info = "\n".join([f"{item.product.name} — {item.quantity} шт. — {item.price} руб." for item in order_items])

    # Подготовка сообщения для администратора
    message = (
        f"Новый заказ #{order.id} от пользователя {order.user.username}\n"
        f"Товары:\n{items_info}\n"
        f"Общая стоимость: {order.total_price} руб.\n"
        f"Адрес доставки: {order.delivery_address}\n"
        f"Дата и время доставки: {order.delivery_date} {order.delivery_time}\n"
        f"Комментарий: {order.comment if order.comment else 'Нет комментария'}"
    )

    # Отправка сообщения в Telegram админу
    bot.send_message(chat_id=settings.ADMIN_CHAT_ID, text=message)
