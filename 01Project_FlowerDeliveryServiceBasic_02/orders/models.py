from django.db import models
from django.conf import settings
from catalog.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from manage_orders.models import ManageOrder


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('notified', 'Уведомление отправлено'),
        ('completed', 'Завершен'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    user_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        formatted_date = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"# {self.id} - {self.product} - {formatted_date}"

@receiver(post_save, sender=Order)
def create_manage_order(sender, instance, created, **kwargs):
    if created:
        ManageOrder.objects.create(
            order_id=instance,
            phone_number=instance.phone_number,
            first_name=instance.first_name,
            last_name=instance.last_name,
            user_comment=instance.user_comment,
        )

