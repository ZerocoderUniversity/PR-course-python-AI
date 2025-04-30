from django.contrib import admin

# Register your models here.
from account.models import User, UserAdmin

admin.site.register(User, UserAdmin)
