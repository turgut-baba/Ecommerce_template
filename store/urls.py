from django.urls import path
from .views import *

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products', ProductView.as_view(), name='products'),
]
