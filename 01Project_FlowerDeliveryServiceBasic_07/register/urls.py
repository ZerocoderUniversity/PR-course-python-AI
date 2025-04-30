from django.urls import path
from .views import register, registration_success, user_login, profile_view, logout_view, index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('register/', register, name='register'),
    path('registration-success/', registration_success, name='registration_success'),
    path('login/', user_login, name='login'),
    path('register/profile/', profile_view, name='profile'),
    path('register/logout/', logout_view, name='logout'),
    

]
