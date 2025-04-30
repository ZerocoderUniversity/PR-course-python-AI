from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    from flowers.models import Flowers
    flowers = models.ManyToManyField(Flowers, through='CartItem')

    def total_price(self):
        return sum([item.flowers.price * item.quantity for item in self.cartitem_set.all()])
class CartItem(models.Model):
    from flowers.models import Flowers
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    flowers = models.ForeignKey(Flowers, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.flowers.price * self.quantity
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'В работе'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f'Order {self.id} by {self.customer_name}'

    def total_price(self):
        # Возвращает сумму всех позиций в заказе
        return self.cart.total_price()

    def get_status_display(self):
        # Возвращает текстовое представление статуса
        return dict(self.STATUS_CHOICES).get(self.status, self.status)