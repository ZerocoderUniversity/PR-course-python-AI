from django.db import models

# Чтение изображения по умолчанию из файла
def get_default_image():
    default_image_path = 'media/catalog/images/default.png'
    with open(default_image_path, 'rb') as image_file:
        return image_file.read()

class Flower(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    image = models.BinaryField(default=get_default_image, verbose_name='Фото')

    def image_preview(self):
        if self.image:
            from django.utils.html import format_html
            import base64
            return format_html('<img src="data:image/png;base64,{}" width="100" height="100"/>',
                               base64.b64encode(self.image).decode('utf-8'))
        return "No Image"

    image_preview.short_description = 'Image Preview'


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Каталог'


    def __str__(self):
        return self.name
