
API_TOKEN = '7198048835:AAEqVEmp7zuYK8VVR0qEPoI5JjqehpblDAw'
API_URL = 'http://127.0.0.1:8000/send_message/'  # URL вашего API

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.conf import settings
from .models import Flower2, Order
from django.contrib.auth.models import User
from django.db import transaction
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

@sync_to_async
def get_product_list():
    with transaction.atomic():
        products = Flower2.objects.all()
        return "\n".join([f"{i+1}. {p.name} - {p.price} руб. {p.description}" for i, p in enumerate(products)])

@sync_to_async
def get_product_by_number(number):
    try:
        return Flower2.objects.all()[int(number) - 1]
    except (IndexError, ValueError):
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text('Приветствуем вас в магазине цветов! Отправьте /order для оформления заказа.')
    elif update.callback_query:
        await update.callback_query.answer('Добро пожаловать в магазин цветов! Отправьте /order для оформления заказа.')

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        product_list = await get_product_list()
        await update.message.reply_text(f"Список доступных товаров:\n{product_list}\n\nДля заказа используйте команду /buy <номер товара>")
    elif update.callback_query:
        product_list = await get_product_list()
        await update.callback_query.answer(f"Список доступных товаров:\n{product_list}\n\nДля заказа используйте команду /buy <номер товара>")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.effective_message.reply_text("Пожалуйста, укажите номер товара после команды /buy")
        return

    product_number = context.args[0]
    product = await get_product_by_number(product_number)

    if product:
        user, _ = await sync_to_async(User.objects.get_or_create)(username=str(update.effective_user.id))
        order = await sync_to_async(Order.objects.create)(user=user)
        if order:
            await sync_to_async(order.products.add)(product)
            order_id = order.id
            await update.message.reply_text(f"Вы заказали {product.name}. Номер вашего заказа: {order_id}")
        else:
            await update.message.reply_text("Извините, произошла ошибка при создании заказа. Пожалуйста, попробуйте еще раз.")
    else:
        await update.message.reply_text("Товар с таким номером не найден. Пожалуйста, проверьте номер и попробуйте снова.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, _ = await sync_to_async(User.objects.get_or_create)(username=str(update.effective_user.id))
    order = await sync_to_async(Order.objects.create)(user=user)
    if order:
        product_names = update.message.text.split(',')
        products = await sync_to_async(Flower2.objects.filter)(name__in=[name.strip() for name in product_names])
        await sync_to_async(order.products.set)(products)
        await update.message.reply_text(f"Заказ оформлен! Номер заказа: {order.id}")
    else:
        await update.message.reply_text("Извините, произошла ошибка при создании заказа. Пожалуйста, попробуйте еще раз.")

def run_bot():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("order", order))
    application.add_handler(CommandHandler("buy", buy))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()
