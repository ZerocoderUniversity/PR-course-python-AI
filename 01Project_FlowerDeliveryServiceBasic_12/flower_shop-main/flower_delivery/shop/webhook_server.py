from flask import Flask, request
import telebot
import logging

app = Flask(__name__)

TELEGRAM_TOKEN = '7159096633:AAEUqc5-pwHXAHjz9MA_raXz_0-6mBe8PZQ'
CHAT_ID = '1072340585'

app = Flask(__name__)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

if __name__ == '__main__':
    app.run(port=5000)