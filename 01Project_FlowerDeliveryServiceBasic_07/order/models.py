from django.db import models
from register.models import User
from catalog.models import Product

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Order {self.id} by {self.user} - {self.address}"
    #def __str__(self):
    #    return f"Order {self.id} by {self.user}"

    @property
    def total_amount(self):
        total = sum(item.total_price for item in self.orderitem_set.all())
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.product.price