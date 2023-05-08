from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Product, get_base_lists, Category
from Ecommerce_Template.settings import STORE_NAME
from django.db.models import Q

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
    template_name = "Test_site/shop-grid.html"
    model = Product

    def get(self, *args, **kwargs):
        context = ProductView.grid_base(self.request)
        item_list = Product.objects.order_by("-rating")

        context.update({
            'Products': item_list,
        })

        return render(self.request, self.template_name, context)

    @staticmethod
    def grid_base(request):
        context = get_base_lists(request)

        latest = Product.objects.order_by("-created_at")[:3]
        latest2 = Product.objects.order_by("-created_at")[3:6]

        context.update({
            'Latest': latest,
            'Latest2': latest2
        })

        return context

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


def product_search(request):  # new
    query = request.GET.get('q')
    context = get_base_lists(request)
    latest = Product.objects.order_by("-created_at")[:3]
    latest2 = Product.objects.order_by("-created_at")[3:6]

    object_list = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    context.update({
        'Products': object_list,
        'Latest': latest,
        'Latest2': latest2
    })
    return render(request, "Test_site/shop-grid.html", context)


def filter_product(request):
    query = request.GET.get('q')
    results = get_base_lists(request)
    #results = Product.objects.filter(models.Q(name__icontains=query) | models.Q(description__icontains=query))

    # Search for products whose name contains all the words in the search query
    keywords = query.split()
    results = Product.objects.filter(name__icontains=keywords[0])
    for keyword in keywords[1:]:
        results = results.filter(name__icontains=keyword)

    # Search for products within a price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    results = Product.objects.filter(price__gte=min_price, price__lte=max_price)