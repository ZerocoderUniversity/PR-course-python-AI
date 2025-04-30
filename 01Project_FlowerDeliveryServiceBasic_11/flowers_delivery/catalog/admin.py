from django.contrib import admin
from .models import Flower
from .forms import FlowerForm

# admin.site.register(Flower)

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    readonly_fields = ('image_preview',)
    form = FlowerForm

    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html
            import base64
            return format_html('<img src="data:image/png;base64,{}" width="100" height="100"/>', base64.b64encode(obj.image).decode('utf-8'))
        return "No Image"
    image_preview.short_description = 'Image Preview'