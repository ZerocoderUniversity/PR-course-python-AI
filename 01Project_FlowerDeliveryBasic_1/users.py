from flask import Flask, request, jsonify
import json
app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    # Получаем данные из запроса
    data = request.get_json()

    # Извлекаем информацию о пользователе
    user_info = {
        'username': data.get('username'),
        'email': data.get('email'),
        'password': data.get('password'),
        'phone': data.get('phone')
    }

    # Здесь вы можете сохранить user_info в базу данных или обработать по-другому
    with open('users.json', 'a') as file:
        file.write(json.dumps(user_info) + '\n')

    print(user_info)  # Для проверки в терминале

    # Возвращаем ответ клиенту
    return jsonify({'status': 'success', 'user_info': user_info})

if __name__ == '__main__':
    app.run(debug=True)