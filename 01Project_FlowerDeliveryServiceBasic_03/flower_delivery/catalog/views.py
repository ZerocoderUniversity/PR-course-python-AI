from django.shortcuts import render
from .models import Flower


def flower_list(request):
    flowers = Flower.objects.all()
    return render(request, 'catalog/flower_list.html', {'flowers': flowers})


from django.shortcuts import render

# Create your views here.
