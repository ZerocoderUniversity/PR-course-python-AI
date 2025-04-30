from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('catalog/', views.catalog, name='catalog'),
    path('order/', views.order, name='order'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('order/', views.order, name='order'),
    path('buyform', views.buyform, name='buyform'),
    path('send_to_telegram/', views.send_to_telegram, name='send_to_telegram'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
