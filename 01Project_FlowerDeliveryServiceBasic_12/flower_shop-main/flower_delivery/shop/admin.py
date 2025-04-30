from django.contrib import admin
from .models import Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image')  # Добавляем поле image
    search_fields = ('name',)
    list_filter = ('price',)
    fields = ('name', 'price', 'image')  # Указываем порядок полей в форме

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)