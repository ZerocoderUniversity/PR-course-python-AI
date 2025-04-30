from django.urls import path
from .views import catalog_view

urlpatterns = [
    path('', catalog_view, name='catalog'),
    ]