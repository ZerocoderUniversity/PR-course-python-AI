from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = ([
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),  # Добавление в корзину
    path('order/create/', views.order_create, name='order_create'),  # Оформление заказа
    path('order/history/', views.order_history, name='order_history'),  # История заказов

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

