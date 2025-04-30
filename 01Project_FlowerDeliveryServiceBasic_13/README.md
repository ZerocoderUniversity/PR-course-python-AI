### Описание проекта

Проект включает разработку интуитивно понятного веб-сайта для удобного заказа цветов с доставкой, а также создание Telegram-бота, который позволит пользователям легко оформлять заказы прямо в мессенджере, получая уведомления и следя за статусом своих покупок.

**Общая архитектура системы:**

- Веб-приложение на Django.
- Серверная часть на Python с использованием Django.
- Модуль регистрации.
- Модуль каталога товаров.
- Модуль оформления заказа.
- Технологии: HTML / Phyton / CSS

### **Установка**

1. Клонирование репозитория

Сначала клонируйте репозиторий с проектом на вашу локальную машину:

```bash
bash
КопироватьРедактировать
git clone <URL_репозитория>
cd flower_delivery

```

---

2. Создание виртуального окружения

Для изоляции зависимостей создайте виртуальное окружение:

```bash
bash
КопироватьРедактировать
python -m venv venv
source venv/bin/activate  # Для Linux / macOS
venv\Scripts\activate  # Для Windows

```

---

3. Установка зависимостей

Установите все необходимые зависимости из файла `requirements.txt`:

```bash
bash
КопироватьРедактировать
pip install -r requirements.txt

```

---

4. Настройка Telegram бота

1. В проекте взаимодействие с Telegram-ботом реализовано в пакете **telebot**.
2. В файле **telebot/config.py** указаны переменные:
    - `TOKEN` — токен вашего Telegram бота.
    - `BOT_ID` — ID вашего бота.
    
    Для получения **ID** вашего бота:
    
    1. Воспользуйтесь API Telegram для поиска ID, как указано в файле **Адрес API для определения ID бота.txt**.
    
    Пример:
    
    ```python
    python
    КопироватьРедактировать
    TOKEN = "your_bot_token"
    BOT_ID = "your_bot_id"
    
    ```
    

---

5. Настройка базы данных

В проекте используется структура базы данных, определённая в файле **models.py**. Включает следующие таблицы:

- **User**: хранит информацию о пользователях.
- **Product**: хранит информацию о букете (название, цена).
- **Order**: хранит информацию о заказах, связанных с пользователями и букетами.

**Пример моделей:**

```python
python
КопироватьРедактировать
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

```

---

6. Миграция базы данных

После настройки базы данных выполните миграции для создания всех необходимых таблиц:

```bash
bash
КопироватьРедактировать
python manage.py makemigrations
python manage.py migrate

```

---

7. Старт сервера

Запустите локальный сервер для проверки работы приложения:

```bash
bash
КопироватьРедактировать
python manage.py runserver

```

Теперь вы можете перейти по адресу `http://127.0.0.1:8000` в вашем браузере и увидеть работу сайта.
