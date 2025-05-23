### Описание проекта

Проект **Flower Delivery** предоставляет удобный веб-интерфейс для выбора и заказа цветов с доставкой, а также интегрированный Telegram-бот для управления заказами и получения уведомлений. Система включает регистрацию пользователей, каталог цветов с фильтрами, корзину для оформления заказов, административную панель для управления товарами и заказами, а также инструменты аналитики и отчетности для отслеживания продаж и заказов.

### **Структура проекта**

Проект построен с использованием фреймворка **Django** на серверной стороне и **Telegram API** для бота. Основные компоненты включают:

- **Django-приложения**:
    - **orders**: управление заказами, продуктами, категориями и отзывами.
    - **users**: управление пользователями и их профилями.
    - **fileviewer**: модуль для работы с файлами и их отображения.
- **Telegram бот**: работает на базе `aiogram`, используется для приема и управления заказами, а также отправки уведомлений.
- **База данных**: используется **SQLite** (возможно, другая СУБД на продакшене).
- **Статические файлы**: стили, иконки, скрипты.
- **Шаблоны**: HTML-шаблоны для рендеринга страниц.

**Основные технологии:**

- **Python** и **Django** для серверной части.
- **HTML/CSS** для фронтенда.
- **aiogram** для интеграции с Telegram.
- **SQLite** как база данных для локальной разработки.

### **Установка**

**Клонирование репозитория**

```
git clone https://github.com/yourusername/flower_delivery.git
cd flower_delivery
```

**Установка зависимостей**

Создайте виртуальное окружение и установите зависимости:

```
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Настройка базы данных**

Примените миграции для настройки базы данных:

```
python manage.py migrate
```

**Создание суперпользователя**

Для доступа к административной панели создайте суперпользователя:

```
python manage.py createsuperuser
```

**Запуск сервера разработки**

Запустите сервер разработки:

```
python manage.py runserver
```

Приложение будет доступно по адресу `http://127.0.0.1:8000/`.
