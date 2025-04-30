from django.core.management.base import BaseCommand
from flower_shop.telegram_bot import run_bot

class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **options):
        self.stdout.write('Запуск Telegram-бота...')
        run_bot()
