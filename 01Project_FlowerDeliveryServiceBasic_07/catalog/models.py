from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=100)
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # новое поле

    def __str__(self):
        return self.name

