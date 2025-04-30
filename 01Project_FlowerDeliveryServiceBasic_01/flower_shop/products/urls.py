from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Список всех товаров
    path('<int:pk>/', views.product_detail, name='product_detail'),  # Подробная информация о товаре
]