from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/<int:product_id>/', views.create_order, name='create_order'),
    path('order/success/', views.order_success, name='order_success'),
    path('repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
]
