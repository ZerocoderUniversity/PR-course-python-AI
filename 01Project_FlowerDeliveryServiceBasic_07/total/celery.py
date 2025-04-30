from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

app = Celery('your_project_name')
# Используем строку для конфигурации, чтобы не возникало проблем с сериализацией
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в приложениях
# app.autodiscover_tasks()