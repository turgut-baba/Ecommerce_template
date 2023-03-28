from django.contrib import admin
from .models import Product


@admin.register(Product)
class RequestAdmin(admin.ModelAdmin):
    product_display = [field.name for field in Product._meta.get_fields()]
