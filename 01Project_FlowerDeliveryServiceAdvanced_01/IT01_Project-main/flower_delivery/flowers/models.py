from django.db import models

class Flowers(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=100)
    main_flowers = models.CharField(max_length=100)
    price = models.IntegerField()
    on_sale = models.BooleanField(default=False)
    image = models.ImageField(upload_to='cat/')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'
# Create your models here.
