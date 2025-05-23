### Описание проекта

**FlowerShop** — это веб-приложение для заказа доставки цветов, интегрированное с Telegram ботом для автоматического получения уведомлений о заказах. Проект разработан с использованием Django для серверной части и `telebot` для взаимодействия с Telegram.

### **Функционал**

- **Регистрация пользователей**: пользователи могут зарегистрироваться и войти в систему.
- **Просмотр каталога цветов**: возможность просматривать доступные букеты и их описание.
- **Оформление заказа**: пользователи могут добавлять букеты в корзину и оформлять заказы.
- **Уведомления о заказах через Telegram бот**: после оформления заказа, бот отправляет уведомление администратору с деталями заказа.

### **Установка**

1. Клонируйте репозиторий:
    
    ```
    git clone https://github.com/NewalexOA/FlowerShop.git
    cd FlowerShop
    ```
    
2. Создайте и активируйте виртуальное окружение:
    
    ```
    python -m venv .venv
    source .venv/bin/activate  # Для Linux и macOS
    .venv\Scripts\activate  # Для Windows
    ```
    
3. Установите зависимости:
    
    ```
    pip install -r requirements.txt
    ```
    
4. Настройте переменные окружения:
    
    Создайте файл `.env` в корневой директории и добавьте следующие строки:
    
    ```
    TELEGRAM_BOT_TOKEN='your_telegram_bot_token'
    
    ```
    
    Замените `your_telegram_bot_token` на токен вашего Telegram бота.
    
5. Запустите скрипт run_once.py для создания суперпользователя и миграций:
    
    ```
    python run_once.py
    ```
    
    Будет создан суперпользователь с именем "admin" и паролем "admin@pass".
    
6. Запустите сервер разработки:
    
    ```
    python manage.py runserver
    ```
    

### **Использование**

1. Перейдите на [http://localhost:8000](http://localhost:8000/) и авторизуйтесь с помощью созданного суперпользователя.
2. Перейдите в админку по ссылке http://localhost:8000/admin/ и создайте товары.
3. **Для администратора:** получите ID чата, куда будут отправляться сообщения, и добавьте его в админке в соответствующее место: [/admin/core/botsettings/](http://localhost:8000/admin/core/botsettings/add/)
4. На сайте просмотрите каталог и добавьте интересующие товары в корзину.
5. Оформите заказ, указав адрес доставки и комментарии.
6. Администратор получит уведомление через Telegram бот с деталями заказа.
