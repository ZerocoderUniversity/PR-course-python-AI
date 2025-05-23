### Описание проекта

**Flower Delivery** — это проект для онлайн-заказа доставки цветов, включающий **веб-приложение на Django** и интегрированный **Telegram-бот** для управления заказами. Мы создали функциональный и удобный сервис для пользователей и администраторов, где каждый шаг продуман для обеспечения лучшего опыта

### **Основные возможности**

**Веб-приложение**

1. **Регистрация и авторизация пользователей** — пользователи могут регистрироваться, входить в систему и изменять данные профиля.
2. **Каталог цветов** — доступен каталог с фотографиями, описаниями и ценами.
3. **Корзина** — добавление товаров в корзину с отображением итоговой суммы заказа.
4. **Оформление заказа** — пользователи могут оформить заказ, указав данные для доставки и комментарии.
5. **История заказов** — просмотр предыдущих заказов, возможность их повторения и отслеживания статуса.
6. **Система отзывов и рейтингов** — пользователи могут оставлять отзывы на товары, помогая другим сделать выбор.
7. **Панель администратора** — управление заказами, изменение их статуса.
8. **Аналитика и отчеты** — отчеты по заказам, доходам и прибыли для административного контроля.

**Telegram-бот**

1. **Получение заказов** — бот принимает заказы и позволяет пользователям выбирать товары из каталога, запрашивая необходимые данные для доставки.
2. **Статус заказов** — уведомляет пользователей о текущем статусе их заказов.
3. **Отчеты для менеджера** — предоставляет администраторам возможность получать отчеты и отслеживать статистику заказов.

---

**Архитектура**

- **Backend**: Django и Django REST Framework для API.
- **Telegram Bot**: Python с использованием `python-telegram-bot` для взаимодействия с пользователями.
- **База данных**: SQLite (или PostgreSQL для production).
- **Frontend**: Шаблоны Django и стилизация с использованием Bootstrap 5 для современного, адаптивного интерфейса.

---

### **Установка и настройка**

**Клонирование репозитория**

`git clone https://github.com/ANVod/flower_delivery.git
cd flower_delivery

Установка зависимостей
Создайте виртуальное окружение и установите зависимости из requirements.txt:
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate     # Для Windows
pip install -r requirements.txt

Переменные окружения
Создайте файл .env в корневой директории и добавьте следующие настройки:
plaintext
DJANGO_SECRET_KEY='your_secret_key'
DEBUG=True
TELEGRAM_BOT_TOKEN='your_telegram_bot_token'
EMAIL_HOST_USER='your_email@gmail.com'
EMAIL_HOST_PASSWORD='your_email_password'

Миграции базы данных
Примените миграции для инициализации базы данных:
python manage.py migrate

Создание суперпользователя
Для доступа к административной панели создайте суперпользователя:
python manage.py createsuperuser

Запуск сервера
Для локального запуска проекта выполните:
python manage.py runserver

Запуск Telegram-бота
Запустите Telegram-бот в отдельном терминале:
python telegram_bot/bot.py`
