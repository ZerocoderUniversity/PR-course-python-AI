import telebot
import logging

# Укажите токен вашего бота
TELEGRAM_TOKEN = '7159096633:AAEUqc5-pwHXAHjz9MA_raXz_0-6mBe8PZQ'
CHAT_ID = '1072340585'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш бот для уведомлений.")

def start_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    start_bot()