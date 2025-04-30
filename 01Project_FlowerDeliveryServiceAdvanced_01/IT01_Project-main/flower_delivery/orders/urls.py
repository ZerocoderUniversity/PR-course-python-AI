from django.urls import path
from .views import add_to_cart, cart_view, order_create, order_success, update_cart_item, orders, order_view,order_repeat

urlpatterns = [
    path('add_to_cart/<int:flowers_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('order/create/', order_create, name='order_create'),
    path('order/success/', order_success, name='order_success'),
    path('cart/update_cart_item', update_cart_item, name='update_cart_item'),
    path('orders/orders', orders, name='orders'),
    path('orders/orders/<int:order_id>', order_view, name='order_view'),
    path('orders/create/<int:order_id>', order_repeat, name='order_repeat'),
]