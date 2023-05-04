from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Product, get_base_lists, Category
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
        context = get_base_lists(self.request)
        featured = Category.objects.all()[:6]
        item_list = Product.objects.order_by("-price")[:8]

        latest1 = Product.objects.order_by("-created_at")[:3]
        latest2 = Product.objects.order_by("-created_at")[3:6]

        rated1 = Product.objects.order_by("-rating")[:3]
        rated2 = Product.objects.order_by("-rating")[3:6]

        context.update({
            'Products': item_list,
            'Featured': featured,
            'Latest1': latest1,
            'Latest2': latest2,
            'Rating1': rated1,
            'Rating2': rated2
        })

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


class ProductDetails(ListView):
    template_name = "Test_site/shop-details.html"
    model = Product

    def get(self, request, slug):
        context = get_base_lists(self.request)
        product = get_object_or_404(Product, slug=slug)
        context.update({
            'Product': product
        })
        return render(self.request, self.template_name, context)
