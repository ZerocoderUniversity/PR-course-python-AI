from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from flower_delivery.utils import send_telegram_message


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    items = instance.cart.cartitem_set.all()
    items_info = [f"{item.flowers.title}: {item.quantity}" for item in items]
    items_message = "\n".join(items_info)

    if created:
        message = (f"Новый заказ создан:\n"
                   f"ID: {instance.id}\n"
                   f"Клиент: {instance.customer_name}\n"
                   f"Телефон: {instance.phone}\n"
                   f"Товары:\n"
                   f" {items_message}\n"
                   f"Адрес доставки: {instance.address}\n"
                   f"Статус: {instance.get_status_display()}")
    else:
        message = (f"Статус заказа изменён:\n"
                   f"ID: {instance.id}\n"
                   f"Клиент: {instance.customer_name}\n"
                   f"Телефон: {instance.phone}\n"
                   f"Новый статус: {instance.get_status_display()}\n"
                   f"Товары:\n"
                   f" {items_message}\n")

    send_telegram_message(message)