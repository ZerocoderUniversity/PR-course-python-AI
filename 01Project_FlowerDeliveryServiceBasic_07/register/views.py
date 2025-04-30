from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from order.models import Order


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Аутентификация и вход пользователя
            user = authenticate(email=user.email, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('catalog')  # Замените 'create_order' на имя вашей целевой страницы
            else:
                print("Аутентификация не удалась")
    else:
        form = UserRegistrationForm()
    return render(request, 'register/register.html', {'form': form})

def registration_success(request):
    return render(request, 'register/registration_success.html')

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalog')  # Перенаправляем пользователя на целевую страницу после успешного входа
        else:
            print("не удалось залогиниться")
    else:
        form = UserLoginForm()
    return render(request, 'register/login.html', {'form': form})

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'register/profile.html', {'orders': orders})

def login_view(request):
    return render(request, 'register/login.html')
@login_required
def logout_view(request):
    print("Вы вышли!")
    logout(request)  # Удаляем аутентификационные данные из сессии
    # Логика выхода пользователя
    return render(request, 'register/login.html')

def index_view(request):
    return render(request, 'register/index.html')