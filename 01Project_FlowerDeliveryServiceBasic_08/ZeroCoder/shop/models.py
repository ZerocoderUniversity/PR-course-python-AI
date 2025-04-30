from django.db import models
from django.contrib.auth.models import User
from .bots.notify_shop import notify_shop


# Модель Product представляет собой товар (букет цветов) в каталоге.

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # Поле для описания товара
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.name


# Модель Order представляет собой заказ, который пользователь может оформить.
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_process', 'In Process'),
        ('delivered', 'Delivered')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=100, blank=True, null=True)  # Telegram ID пользователя
    products = models.ManyToManyField(Product)  # Связь с товарами
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    delivery_address = models.CharField(max_length=255, blank=False, null=False)  # Адрес доставки
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Общая сумма
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"