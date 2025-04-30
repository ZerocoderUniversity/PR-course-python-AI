from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import logging
from forms.models import Order
from django.utils import timezone

# Включить логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Привет! Добро пожаловать в наш цветочный магазин. Пожалуйста, пришлите ваш заказ в формате: "Букет, Адрес доставки, Дата доставки, Имя, Телефон"')

# Обработка текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    try:
        bouquet_name, delivery_address, delivery_date, customer_name, customer_phone = map(str.strip, text.split(','))
        # Преобразование даты из строки в объект datetime
        delivery_date = timezone.datetime.strptime(delivery_date, '%Y-%m-%d %H:%M')

        # Создание заказа
        order = Order(

            #bouquet_name=bouquet_name,
            #delivery_address=delivery_address,
            #delivery_date=delivery_date,
            #customer_name=customer_name,
            #customer_phone=customer_phone
        )
        order.save()

        update.message.reply_text('Ваш заказ был успешно создан!')
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        update.message.reply_text('Ошибка обработки заказа. Пожалуйста, используйте правильный формат.')

def main() -> None:
    # Инициализация бота
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
    dispatcher = updater.dispatcher

    # Обработчики команд и сообщений
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
