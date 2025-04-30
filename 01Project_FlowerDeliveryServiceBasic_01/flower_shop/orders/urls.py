from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),  # Маршрут для оформления заказа
    path('<int:pk>/', views.order_detail, name='order_detail'),  # Подробности заказа
]