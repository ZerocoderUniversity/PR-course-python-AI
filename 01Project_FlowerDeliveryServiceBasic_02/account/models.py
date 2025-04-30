from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin

class User(AbstractUser):
    phone_number = models.CharField(max_length=12, blank=True, null=True, verbose_name="Номер телефона")
    username = models.CharField(max_length=150, unique=True, verbose_name='Логин')
    email = models.EmailField(max_length=254, verbose_name='Ваш e-mail')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
