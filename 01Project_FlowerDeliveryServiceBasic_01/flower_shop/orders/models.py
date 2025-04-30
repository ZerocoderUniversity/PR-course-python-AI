from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class Order(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Product')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField()

    def clean(self):
        current_time = now().time()
        start_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = current_time.replace(hour=23, minute=0, second=0, microsecond=0)
        if not (start_time <= current_time <= end_time):
            raise ValidationError('Заказы можно оформлять только в рабочее время с 9:00 до 23:00.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ {self.id} от {self.user}"
