from django.test import TestCase
import unittest
from django.test import TestCase
from django.urls import reverse
from .models import Flowers

class ViewsTestCase(TestCase):

    def setUp(self):
        # Создаем несколько объектов Flowers для тестирования
        Flowers.objects.create(title="Роза", short_description="Красный",price=1000,on_sale=True,image='static/flowers/img/cat/rose1.jpg' )
        Flowers.objects.create(title="Тюльпан", short_description="Желтый",price=2000,on_sale=True,image='static/flowers/img/cat/rose2.jpg' )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flowers/index.html')
        self.assertContains(response, "Главная")

    def test_catalog_view(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flowers/catalog.html')
        self.assertContains(response, "Роза")
        self.assertContains(response, "Тюльпан")

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flowers/about.html')
        self.assertContains(response, "О нас")

    def test_delivery_view(self):
        response = self.client.get(reverse('delivery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flowers/delivery.html')
        self.assertContains(response, "Доставка и оплата")

if __name__ == '__main__':
    unittest.main()