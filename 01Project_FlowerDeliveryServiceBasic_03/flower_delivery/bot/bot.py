from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()
from catalog.models import Flower, Order

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to the Flower Delivery Bot!")

@dp.message_handler(commands=['flowers'])
async def list_flowers(message: types.Message):
    flowers = Flower.objects.all()
    response = "Список доступных цветов:\n"
    for flower in flowers:
        response += f"{flower.name} - {flower.price} руб.\n"
    await message.reply(response if flowers else "Цветы отсутствуют.")

@dp.message_handler(commands=['orders'])
async def list_orders(message: types.Message):
    orders = Order.objects.all()
    response = "Список заказов:\n"
    for order in orders:
        response += f"{order.flower.name} - {order.quantity} шт. - {order.quantity * order.flower.price} руб.\n"
    await message.reply(response if orders else "Заказы отсутствуют.")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)