from django.shortcuts import render
from .models import Flowers
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
def index(request):
    return render(request, "flowers/index.html", {"title": "Главная"})

def catalog(request):
    flowers = Flowers.objects.all()
    return render(request, "flowers/catalog.html",  {"flowers": flowers})

def about(request):
    return render(request, "flowers/about.html", {"title": "О нас"})

def delivery(request):
    return render(request, "flowers/delivery.html", {"title": "Доставка и оплата"})