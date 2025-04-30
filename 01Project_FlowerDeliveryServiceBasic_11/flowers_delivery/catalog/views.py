from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Flower
from PIL import Image
import io

from django.views.generic import ListView, DetailView

def image_view(request, pk):
    obj = get_object_or_404(Flower, pk=pk)
    image_data = obj.image
    image = Image.open(io.BytesIO(image_data))
    format_to_content_type = {
        'JPEG': 'image/jpeg',
        'PNG': 'image/png',
        'GIF': 'image/gif',
        # можно добавить другие форматы, если необходимо
    }
    content_type = format_to_content_type.get(image.format, 'application/octet-stream')
    return HttpResponse(image_data, content_type=content_type)


class ProductListView(ListView):
    model = Flower
    template_name = 'catalog/flower_list.html'


class ProductDetailView(DetailView):
    model = Flower
    template_name = 'catalog/product_detail.html'


def flower_list(request):
    flowers = Flower.objects.all()

    return render(request, 'catalog/flower_list.html', {'flowers': flowers})


def home(request):
    return render(request, 'catalog/home.html')