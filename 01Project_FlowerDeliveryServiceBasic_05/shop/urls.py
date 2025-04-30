from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('orders/', views.orders, name='orders'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('add_to_shopping/', views.add_to_shopping, name='add_to_shopping'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('send-orders-to-telegram/', views.send_orders_to_telegram, name='send_orders_to_telegram'),
]