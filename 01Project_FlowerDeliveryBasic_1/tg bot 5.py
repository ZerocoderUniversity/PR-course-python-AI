import telebot
from telebot import types

phone2 = ''

bot = telebot.TeleBot('7346026260:AAFkDie023ZDmarmPuSk6FsYpdy7Ef-cY4M')


@bot.message_handler(commands=['number'])
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, 'Номер телефона', reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        print(message.contact)
        phone2 = message.contact
        print(phone2[0])