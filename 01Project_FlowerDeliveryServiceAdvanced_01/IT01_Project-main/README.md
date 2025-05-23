Этот репозиторий содержит выпускной проект к курсу Программист на Python с нуля с помощью ChatGPT в университете Zerocoder
Реализован вариант Advanced. ТЗ приведено ниже. 
Для отправки сообщений в телеграм бот необходимо в папку flower_delivery добавить файл config.py где будут указаны токен бота и номера чата с магазином, в который нужно отправлять сообщения. Содержание этого файла должно быть таким:
TOKEN = 'API-KEY'
CHAT_ID = chat_id

Номер чата можно получить , например при помощи функции getUpdates, отправив запрос: 
 https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates

В этом проекте применены следующие основные сущности : 
flowers - букеты , основной вид товаров на этом сайте 
user - пользователи , стандратный справочник Django
profiles - профили , дополнительный справочник , связанный со справочником пользователи, для хранения дополнительной информации
cart_item - справочник для хранения единиц товаров в конкректной корзине
cart - справочник корзин, в которых хранятся cart_item
orders - справочник заказов 

Реализовано три приложения : 
users - здесь собраны данные  и обработка данных связанные с пользователями (регистрация , вход)
flowers - здесь собраны данные связанные с каталогом и основными страницами сайта 
orders - здесь собраны данные связанные с корзиной , товарами в корзине и созданием и управлением заказами

Дополнительно реализована возможность ограничения продажи букетов, которых нет в наличии (дополнительный признак в каталоге)

Для администрирования используется стандартная админ панель Django (в данном проекте  логин admin , пароль 123 )
 
Техническое задание FlowerDelivery Advanced:
Сайт с доставкой цветов и получение заказов через Telegram бота

Цель проекта:
Создание веб-сайта для заказа доставки цветов с расширенной интеграцией заказов через Telegram бота.

Общая информация о проекте:
Проект включает разработку веб-сайта для заказа цветов и продвинутого Telegram бота для приема и управления заказами.

Область применения
Описание проблемы:
Необходимость удобного и быстрого способа заказа цветов через интернет и мессенджер.

Пользователи системы:
Частные лица и компании.

Основные ограничения и допущения:
Пользователи должны иметь доступ к интернету и Telegram. Заказы принимаются только в рабочее время.

Функциональные требования
- Веб-сайт:
    - Регистрация и авторизация пользователей.
    - Просмотр каталога цветов.
    - Выбор цветов и добавление в корзину.
    - Оформление заказа с указанием данных для доставки.
    - Просмотр истории заказов.
    - Аккаунт администратора для отметки статуса заказа
    - Возможность повторного заказа, той же позиции из каталога.
- Telegram бот:
    - Получение заказов с информацией о букетах и доставке.
    - Уведомления о статусе заказа.

Общая архитектура системы:
- Веб-приложение на Django.
- Серверная часть на Python с использованием Django.
- Описание подсистем и модулей:
- Модуль регистрации и авторизации.
- Модуль каталога товаров.
- Модуль оформления заказа.
- Модуль управления заказами.

Модель данных:
- Таблица пользователей (ID, имя, email, телефон, адрес).
- Таблица товаров (ID, название, цена, изображение).
- Таблица заказов (ID, пользователь, товары, статус, дата заказа).

Методы и стратегии тестирования:
- Юнит-тестирование.
- Интеграционное тестирование.
