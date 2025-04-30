# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order
# from .telegram_bot import notify_telegram
#
# @receiver(post_save, sender=Order)
# def order_created2(sender, instance, created, **kwargs):
#     if created:
#         message = f'Новый заказ создан: {instance}'
#         notify_telegram(message)