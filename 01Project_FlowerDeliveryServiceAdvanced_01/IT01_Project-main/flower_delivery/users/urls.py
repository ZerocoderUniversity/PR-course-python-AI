from django.urls import path, include
from .views import register, user_login ,user_logout, user_profile, edit_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('profile_edit/', edit_profile, name='edit_profile'),

]