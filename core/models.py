from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from store.models import CartItem, Product, validate_rating
from django.contrib.auth.models import AbstractUser
from enum import IntEnum
from django.utils.timezone import now
from django_countries.fields import CountryField
from decimal import Decimal

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Address(models.Model):
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.street_address.name + " " + self.apartment_address.name

    class Meta:
        verbose_name_plural = 'Addresses'


class Customer(AbstractUser):
    address_info = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    cart = models.ManyToManyField(CartItem) #on_delete=models.CASCADE)
    favourites = models.ManyToManyField(Product)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    desc = models.CharField(max_length=100, unique=False, default="Please enter a description.")

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    created_at = models.DateTimeField(default=now)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal('0.0'), validators=[validate_rating])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.product}'