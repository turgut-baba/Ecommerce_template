from django.urls import path
from .views import *

app_name = 'store'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('products', ProductView.as_view(), name='products'),
]
