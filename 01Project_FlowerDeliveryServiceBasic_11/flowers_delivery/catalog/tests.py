# Тесты для models
from django.test import TestCase

from .models import Flower
import base64

class FlowerModelTest(TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.flower = Flower.objects.create(
            name="Роза",
            description="Красная роза",
            price=10.00,
            image=base64.b64encode(b'TestImageData')
        )

    def test_flower_creation(self):
        """Проверка, что объект Flower был успешно создан"""
        self.assertEqual(self.flower.name, "Роза")
        self.assertEqual(self.flower.description, "Красная роза")
        self.assertEqual(self.flower.price, 10.00)
        self.assertEqual(base64.b64decode(self.flower.image), b'TestImageData')

    def test_image_preview(self):
        """Проверка метода image_preview"""
        expected_html = '<img src="data:image/png;base64,{}" width="100" height="100"/>'.format(
            base64.b64encode(b'TestImageData').decode('utf-8')
        )
        self.assertEqual(self.flower.image_preview(), expected_html)

    def test_image_preview_no_image(self):
        """Проверка метода image_preview при отсутствии изображения"""
        flower_no_image = Flower.objects.create(
            name="Лилия",
            description="Белая лилия",
            price=15.00
        )
        self.assertEqual(flower_no_image.image_preview(), "No Image")


# Тесты для urls
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from . import views

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_flower_list_url_is_resolved(self):
        url = reverse('flower_list')
        self.assertEqual(resolve(url).func, views.flower_list)

    def test_image_view_url_is_resolved(self):
        url = reverse('image_view', args=[1])
        self.assertEqual(resolve(url).func, views.image_view)


# Тесты для views
from django.test import TestCase, Client
from django.urls import reverse
from .models import Flower
from PIL import Image
import io


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.flower = Flower.objects.create(name='Test Flower', image=b'test_image_data')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/home.html')

    def test_flower_list_view(self):
        response = self.client.get(reverse('flower_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/flower_list.html')

    def test_image_view(self):
        response = self.client.get(reverse('image_view', args=[self.flower.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/octet-stream')

    def test_product_list_view(self):
        response = self.client.get(reverse('flower_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/flower_list.html')

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.flower.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_detail.html')