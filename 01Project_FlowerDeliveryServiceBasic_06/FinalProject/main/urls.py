
from django.urls import path
from . import views


urlpatterns = [


    path('', views.index, name='home'),
    path('new/', views.new, name='page2'),
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('product_list/', views.product_list, name='product_list'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),


]
