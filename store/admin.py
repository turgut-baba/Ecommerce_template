from django.contrib import admin
from .models import Product, Category


@admin.register(Product, Category)
class RequestAdmin(admin.ModelAdmin):
    product_display = [field.name for field in Product._meta.get_fields()]
    category_display = [field.name for field in Category._meta.get_fields()]
