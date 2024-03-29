from django.urls import path
from .views import (
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    # PaymentView,
    # AddCouponView,
    # RequestRefundView,
    login_view,
    register_view,
    cart_view,
    profile_view,
    logout_view
)

app_name = 'core'

urlpatterns = [
    # path('checkout/', CheckoutView.as_view(), name='checkout'),
    #path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    # path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    # path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    # path('request-refund/', RequestRefundView.as_view(), name='request-refund'),

    path('login', login_view, name="login"),
    path('register', register_view, name="register"),
    path('cart', cart_view, name='cart'),
    path('profile', profile_view, name="profile"),
    path('logout', logout_view, name='logout')
]