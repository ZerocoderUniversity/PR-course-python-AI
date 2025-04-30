from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Flower2(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image_link = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Flower2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class Select_shop(models.Model):
    products = models.ManyToManyField(Flower2)


    def __str__(self):
        return self.products


