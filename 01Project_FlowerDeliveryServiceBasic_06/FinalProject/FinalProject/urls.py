from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
##from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
   ## path('register/', views.register, name='register'),
   ##path('catalog/', views.catalog, name='catalog'),
    ##path('order/', views.create_order, name='create_order'),
    path('', include('main.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
