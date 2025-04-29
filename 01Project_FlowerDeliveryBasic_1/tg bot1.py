import threading

import telebot
import logging
from flask import Flask, request, jsonify
from threading import Thread, Lock


name = '';
surname = '';
age = 0;
CHAT_ID = '';

app = Flask(__name__)
@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.json
    order_details = data.get('orderDetails', '')
    CHAT_ID_CUSTOMER = data.get('CHAT_ID', '')
    message = f'Вы оформили заказ:\n{order_details}'

bot = telebot.TeleBot('7346026260:AAFkDie023ZDmarmPuSk6FsYpdy7Ef-cY4M');
markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1 = telebot.types.KeyboardButton('Запуск')
itembtn2 = telebot.types.KeyboardButton('Сделать заказ')
itembtn3 = telebot.types.KeyboardButton('Привет')
itembtn4 = telebot.types.KeyboardButton('/reg')
markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите опцию из меню ниже.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Запуск')
def handle_start(message):
    bot.send_message(message.chat.id, "Бот запущен!")


@bot.message_handler(func=lambda message: message.text == 'Сделать заказ')
def handle_order(message):
    bot.send_message(message.chat.id, "Пожалуйста, укажите детали вашего заказа.")
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, приятно познакомиться ")
    elif message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name);
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help или /reg.")



def get_name(message): #получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id,'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    global age;
    while age == 0: #проверяем что возраст изменился
        try:
             age = int(message.text) #проверяем, что возраст введен корректно
             CHAT_ID = message.from_user.id;

        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
        bot.send_message(message.from_user.id, 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?')

def start_bot_tread():
    print("Start TG Bot")
    bot.polling(none_stop=True, interval=0)
def start_flask_tread():
    print('Start Flask on 5000 port')
    app.run(debug=True)

if __name__ == '__main__':
    t1 = threading.Thread(target=start_bot_tread, args=(), daemon=True)
    t2 = threading.Thread(target=start_flask_tread, args=(), daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

