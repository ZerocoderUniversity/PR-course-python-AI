import requests
from flower_delivery.config import TOKEN, CHAT_ID

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
CHAT_ID = CHAT_ID

def send_telegram_message(message):
    print('ТГбот ')
    print(message)
    print(TELEGRAM_API_URL)
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(TELEGRAM_API_URL, data=payload)