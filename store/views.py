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


def main_page(request):
    """
    featured = Item.objects.order_by('-is_featured')
    context = {
        'featured_items': featured
    }
    :param request:
    :return:
    """
    return render(request, "store/main_page.html", settings)


class ProductView(ListView):
    template_name = "store/products.html"
    model = Product

    def head(self, *args, **kwargs):
        products = self.get_queryset().latest('publication_date')
        response = HttpResponse(
            headers={'Last-Modified': products.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')},
        )
        return response


def cart_view(request):
    return render(request, "store/cart.html", settings)

