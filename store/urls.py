from django.urls import path
from .views import *

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>', ProductDetails.as_view(), name='product_view'),
    path('products', ProductView.as_view(), name='products'),
    path('search', product_search, name='search')
]
