from django.contrib import admin
from .models import ManageOrder

class ManageOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'first_name', 'last_name', 'phone_number', 'status']
    readonly_fields = ('order_id', 'phone_number', 'first_name', 'last_name', 'user_comment')
    fields = ('status', 'manager_comment', 'order_id', 'phone_number', 'first_name', 'last_name', 'user_comment')
    list_filter = ('status',)

    def order_id(self, obj):
        return obj.order_id.order_number
    order_id.short_description = 'Заказ №'

admin.site.register(ManageOrder, ManageOrderAdmin)