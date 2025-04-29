import telebot
from flask import Flask, request, jsonify

app = Flask(__name__)
bot = telebot.TeleBot('7346026260:AAFkDie023ZDmarmPuSk6FsYpdy7Ef-cY4M')
@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.json
    order_details = data.get('orderDetails', '')
    CHAT_ID_CUSTOMER = data.get('CHAT_ID', '')
    message = f'Вы оформили заказ:\n{order_details}'# Здесь предполагается, что вы отправите сообщение клиенту через Telegram API
    bot.send_message(CHAT_ID_CUSTOMER, message)
    return jsonify({"status": "success", "message": message})

def start_flask():
    print('Start Flask on 5000 port')
    app.run(debug=True)

if __name__ == '__main__':
    start_flask()

