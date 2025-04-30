import os
import django
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
from asgiref.sync import sync_to_async

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerDeliverySite.settings')
django.setup()

from shop.models import Order  # Импортируйте необходимые модели

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для старта бота
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Доброго время суток, {message.from_user.full_name}! "
        f"\n Добро пожаловать в Магазин цветов Bernardo's Flowers! Кликните по /order чтобы посмотреть ваш заказ."
    )

@dp.message(Command('photo'))
async def photo(message: Message):
    rand_photo = 'shop/media/media/flowers/Rob3YgoHjz_GcBpfxY.jpg'
    photo_file = FSInputFile(rand_photo)
    await message.answer_photo(photo=photo_file, caption='Это супер крутая картинка')

# Функция для обработки нового заказа
@dp.message(Command('order'))
async def order(message: Message):
    # Получаем последний заказ
    order = await sync_to_async(Order.objects.last)()

    if order:
        # Соберем информацию о заказе
        flowers_info = ""
        flowers = await sync_to_async(list)(order.flowers.all())  # Получаем все цветы асинхронно

        for flower in flowers:
            flowers_info += f"Название: {flower.name}\nЦена: {flower.price}₽"
            path_to_image = flower.image.path
            # print(f"Path to image: {path_to_image}")

        message_text = f"Ваш заказ №: {order.id}\n{flowers_info}\nЗаказ создан: {order.created_at.date()}"
        # print(message_text)

        await message.answer(f"{message_text}")

        # path_2 = 'shop/media/media/flowers/Rob3YgoHjz_GcBpfxY.jpg'
        photo = FSInputFile(path_to_image)
        await message.answer_photo(photo=photo, caption="Ваш букет!")

    else:
        await message.answer("Нет доступных заказов.")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запуск бота
    asyncio.run(main())