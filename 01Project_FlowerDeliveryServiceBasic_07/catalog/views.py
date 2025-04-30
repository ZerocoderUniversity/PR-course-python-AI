from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product



# Create your views here.

def catalog_view(request):
    products = Product.objects.all()
    return render(request, "catalog/catalog.html", {"products":products})

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'product_list.html', {'products': products})