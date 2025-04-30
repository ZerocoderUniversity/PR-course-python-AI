from django.contrib import admin
from .models import Flower2, Order



# Register your models here.
@admin.register(Flower2)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image_link')
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    filter_horizontal = ('products',)