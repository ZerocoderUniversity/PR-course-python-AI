import requests
TOKEN = "7346026260:AAFkDie023ZDmarmPuSk6FsYpdy7Ef-cY4M"
chat_id = "7346026260"
message = "Тест"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print(requests.get(url).json()) # Эта строка отсылает сообщение