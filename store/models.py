from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.timezone import now
import os
from Ecommerce_Template import settings
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import DecimalValidator

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


def get_base_lists(request) -> dict:
    categories = Category.objects.order_by("-title")

    from payments.models import Order

    if request.user.is_authenticated:
        cart, created = Order.objects.get_or_create(user=request.user)

    try:
        all_items = cart.items.all()
        cart_quant = 0

        for item in all_items:
            cart_quant += item.quantity

    except (AttributeError, UnboundLocalError) as e:
        cart_quant = 0

    try:
        fav_quant = request.user.favourites.count()
    except AttributeError:
        fav_quant = 0

    return {
        'Categories': categories,
        'cart_quant': cart_quant,
        'fav_quant': fav_quant
        }


def validate_rating(value):
    # Round the value to one decimal place
    rounded = Decimal(value).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    # Check if the rounded value is within the valid range
    if not Decimal('0.0') <= rounded <= Decimal('5.0'):
        raise ValidationError('Rating must be between 0.0 and 5.0 with one decimal place.')


class Category(models.Model):
    title = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=3)
    image = models.ImageField(upload_to="media/category", default=os.path.join(settings.STATIC_URL, 'img/default/category.png'))

    def __str__(self):
        return self.abbreviation


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal('0.0'), validators=[validate_rating])
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="media/products", default=os.path.join(settings.STATIC_URL, 'img/default/product.png'))

    stripe_product_id = models.CharField(max_length=100, default="NULL")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
