from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from .models import Product, Category
from Ecommerce_Template.settings import STORE_NAME

settings = {
    'Title': STORE_NAME
}

def packed_context(cont: dict) -> dict:
    global settings
    context = cont | settings
    return context



class HomeView(ListView):
    model = Product
    paginate_by = 10
    template_name = "Test_site/index.html"

    def get(self, *args, **kwargs):
        item_list = Product.objects.order_by("-price")
        categories = Category.objects.order_by("-title")

        latest1 = Product.objects.order_by("-created_at")[:3]
        latest2 = Product.objects.order_by("-created_at")[3:6]

        rated1 = Product.objects.order_by("-rating")[:3]
        rated2 = Product.objects.order_by("-rating")[3:6]

        context = {
            'Products': item_list,
            'Categories': categories,
            'Latest1': latest1,
            'Latest2': latest2,
            'Rating1': rated1,
            'Rating2': rated2,
        }
        return render(self.request, self.template_name, context)


class ProductView(ListView):
    template_name = "store/shop-grid.html"
    model = Product

    def head(self, *args, **kwargs):
        products = self.get_queryset().latest('publication_date')
        response = HttpResponse(
            headers={'Last-Modified': products.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')},
        )
        return response
