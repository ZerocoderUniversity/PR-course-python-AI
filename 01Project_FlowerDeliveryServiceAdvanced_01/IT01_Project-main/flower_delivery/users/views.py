from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserProfileForm, ProfileForm

def register(request):
    error = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')  # замените на вашу страницу
        else:
            error = form.errors
    else:
            form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form,'error': error})


def user_login(request):
    error=''
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
        else:
            error = form.errors
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form, 'error': error})

def user_logout(request):
    logout(request)
    return redirect('index')

def user_profile(request):
    return render(request, 'users/profile.html')


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'users/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })