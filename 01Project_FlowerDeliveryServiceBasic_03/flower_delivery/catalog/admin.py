from django.contrib import admin
from .models import Flower, Order
from django.contrib.admin import AdminSite

admin.site.register(Flower)
admin.site.register(Order)

# Переопределение заголовка
class MyAdminSite(AdminSite):
    site_header = "Администрирование"
    site_title = "Администрирование"
    index_title = "Администрирование сайта"

admin_site = MyAdminSite(name='myadmin')

# Register your models here.
