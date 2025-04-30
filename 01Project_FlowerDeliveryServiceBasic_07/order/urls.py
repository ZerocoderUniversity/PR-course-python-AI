from django.urls import path, include
from .views import create_order, order_success, cart_add, cart_detail, cart_remove, order_create, decrement_view

urlpatterns = [
    path('', create_order, name='create_order'),
    path('order-success/', order_success, name='order_success'),
    path('orders/cart/add/<int:product_id>/', cart_add, name='add_to_cart'),
    path('orders/cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('orders/cart/decrement/<int:product_id>/', decrement_view, name='decrement'),
    path('orders/cart/', cart_detail, name='cart_detail'),
    path('order/create/', order_create, name='order_create'),
]