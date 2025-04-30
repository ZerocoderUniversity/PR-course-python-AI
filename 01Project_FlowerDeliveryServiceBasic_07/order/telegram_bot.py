import threading
from aiogram import Bot
from total.config import BOT_TOKEN, CHAT_ID
import asyncio

async def send_telegram_message(message):
    bot = Bot(token=BOT_TOKEN)
    try:
        await asyncio.sleep(5)
        await bot.send_message(chat_id=CHAT_ID, text=message)
    finally:
        await bot.close()

def notify_telegram(message):
    thread = threading.Thread(target=asyncio.run, args=(send_telegram_message(message),))
    thread.start()
