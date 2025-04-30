from django.contrib import admin
from django.utils.html import format_html
from django.contrib import admin
from .models import Product, Order
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'image_tag')  # Добавляем отображение изображения
    list_filter = ('available', 'created', 'updated')
    search_fields = ('name', 'description')

    # Отображение миниатюры изображения в админке
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Image'

# Настройка отображения заказов (Order) в админ-панели
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')  # Поля для отображения в списке
    list_filter = ('status', 'created_at')  # Фильтры по статусу и дате создания
    search_fields = ('user__username', 'delivery_address')  # Поиск по пользователю и адресу доставки
    readonly_fields = ('total_price', 'created_at')  # Поля, которые нельзя редактировать вручную
    ordering = ('-created_at',)  # Сортировка по дате создания

    # Добавляем отображение товаров в заказе на странице заказа в админке
    def products_list(self, obj):
        return ", ".join([product.name for product in obj.products.all()])
    products_list.short_description = 'Products'  # Название колонки в админке

#admin.site.register(Product)
#admin.site.register(Order)

