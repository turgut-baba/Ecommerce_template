from django.urls import path
from .views import *

app_name = 'payments'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]