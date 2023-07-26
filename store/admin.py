from django.contrib import admin
from .models import Product, Category
from django.utils.text import slugify


@admin.register(Category)
class RequestAdmin(admin.ModelAdmin):
    category_display = [field.name for field in Category._meta.get_fields()]


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)


admin.site.register(Product, ProductAdmin)
