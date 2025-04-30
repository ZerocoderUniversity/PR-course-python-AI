from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Flower, Order
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import OrderForm
from django.contrib import messages
from .forms import UserRegisterForm

import requests


def home(request):
    return render(request, 'main/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'main/catalog.html', {'flowers': flowers})


def buyform(request):
    return render(request, 'main/buyform.html', {'buyform': buyform})


@login_required
def order(request):
    if request.method == 'POST':
        flower_ids = request.POST.getlist('flowers')
        flowers = Flower.objects.filter(id__in=flower_ids)
        order = Order.objects.create(user=request.user)
        order.flowers.set(flowers)
        return redirect('home')
    else:
        flowers = Flower.objects.all()
    return render(request, 'main/order.html', {'flowers': flowers})


def send_to_telegram(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')

            # Отправка данных в Telegram
        telegram_token = '7235687275:AAEcwBoKqnq55vOcqvsO0DG1b_4KCwAjVvU'
        chat_id = '686562348'
        telegram_url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'

        text = f"Подтверждение Вашего заказа: {name} в магазине Flower-Delivery \nАдрес доставки: {message}"

        requests.post(telegram_url, data={'chat_id': chat_id, 'text': text})

        return render(request, 'main/catalog.html', {'catalog': catalog})
    else:
        return HttpResponse("Используйте POST запрос для отправки данных.")


