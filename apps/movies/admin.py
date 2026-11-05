from django.contrib import admin
from .models import Categories, Movies


# Register your models here.

@admin.register(Categories, Movies)
class BaseAdminRegister(admin.ModelAdmin):
    pass
