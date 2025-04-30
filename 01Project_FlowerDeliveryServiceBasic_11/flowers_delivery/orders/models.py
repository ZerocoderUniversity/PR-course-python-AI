from django.db import models
from catalog.models import Flower
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    recipient_name = models.CharField(max_length=100, default='Получатель не указан', verbose_name='Имя получателя')
    address = models.CharField(max_length=255, default='Адрес не указан', verbose_name='Адрес доставки')
    phone = models.CharField(max_length=15, default='Телефон не указан', verbose_name='Телефон получателя')


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ #{self.id} от {self.user} для {self.recipient_name}"


