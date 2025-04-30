from django.shortcuts import render

def index(request):
    return render(request, 'base/index.html')

def about(request):
    return render(request, 'base/about.html')

def contacts(request):
    return render(request, 'base/contacts.html')