import random
import string

# import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

from store.models import Product, get_base_lists
from payments.models import Order, OrderItem
from .forms import RegistrationForm, AddressForm
from django.contrib.auth import authenticate, login, logout
from .models import Device
from django_countries.data import COUNTRIES
# Can be custom.
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail


# ===================================================================================
# Authentication systems.
# ===================================================================================


def auth_status(request, for_user: bool = True):
    if request.user.is_authenticated:
        return None if for_user is False else request.user
    else:
        device_name = request.COOKIES['device']

        device_obj, created = Device.objects.get_or_create(
            name=device_name
        )

        return None if for_user is True else device_obj


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('store:home')
        else:
            context = {'Error': 'Invalid login!'}
            return render(request, 'Test_site/login.html', context)
    else:
        # Render the login template
        return render(request, 'Test_site/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                'Welcome to MySite',
                'Thank you for registering. Your username is {}.'.format(user.username),
                'turgutbababalim@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('store:home')
    else:
        form = RegistrationForm()
    return render(request, 'Test_site/register.html', {'form': form})


def forgot_password(request):
    ...


@login_required
def profile_view(request):
    context = get_base_lists(request)
    orders = Order.objects.filter(user=request.user)
    addresses = request.user.addresses.all()
    context.update({"Orders": orders, "Addresses": addresses})

    return render(request, 'Test_site/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('store:home')


@login_required
def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            print("Valid")
            address = form.save()
            user_profile = request.user
            user_profile.addresses.add(address)
            user_profile.save()

            return redirect('core:profile')  # Redirect to the user's profile page
        else:
            messages.error(request, "Error")
    else:
        form = AddressForm()

    context = get_base_lists(request)
    context.update({'form': form, 'countries': COUNTRIES})
    return render(request, 'Test_site/add-address.html', context)


@login_required
def remove_address_view(request, title):
    address = request.user.addresses.all()

    for address in address:
        if address.title == title:
            request.user.addresses.remove(address)

    return redirect('core:profile')


# ===================================================================================
# Order views.
# ===================================================================================


def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)

    if request.user.is_authenticated:
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )

        order_qs = Order.objects.filter(user=request.user, ordered=False)
    else:
        device_name = request.COOKIES['device']

        device_obj, created = Device.objects.get_or_create(
            name=device_name
        )
        # customer, created = Customer.objects.get_or_create(device=device)

        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=None,
            device=device_obj,
            ordered=False
        )

        order_qs = Order.objects.filter(device=device_obj, user=None, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:cart")
    else:
        ordered_date = timezone.now()
        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
        else:
            order = Order.objects.create(
                device=device_obj, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:cart")


@login_required
def update_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:cart")


def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=auth_status(request),
        device=auth_status(request, False),
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=auth_status(request),
                device=auth_status(request, False),
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def cart_view(request):
    context = get_base_lists(request)

    if request.user.is_authenticated:
        cart, created = Order.objects.get_or_create(user=request.user)
    else:
        device_name = request.COOKIES['device']
        device_obj, created = Device.objects.get_or_create(
            name=device_name
        )
        cart, created = Order.objects.get_or_create(
            device=device_obj,
            defaults={'ordered_date': timezone.now()}
        )

    if not created:
        cart_items = cart.items.all()

        context.update({
            'CartItems': cart_items
        })

    return render(request, "Test_site/shoping-cart.html", context)
