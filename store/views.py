from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from .models import Product
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
        item_list = Product.objects.order_by("price")
        context = {
            'Products': item_list
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
