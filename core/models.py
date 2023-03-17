from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from store.models import CartItem
from django.contrib.auth.models import AbstractUser

from enum import Enum

class AuthLevel(Enum):
    Customer = 1
    Worker = 2
    Admin = 3
    Programmer = 4

class Customer(AbstractUser):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    cart = models.ManyToManyField(CartItem) #on_delete=models.CASCADE)
    auth_level = AuthLevel.Customer

    def __str__(self):
        return self.user.username


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Customer = Customer.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class Worker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auth_level = AuthLevel.Worker


class Admin(models.Model):
    auth_level = AuthLevel.Admin


class Owner(models.Model):
    auth_level = AuthLevel.Admin


class Programmer(Owner):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    auth_level = AuthLevel.Programmer

    def __str__(self):
        return self.user.username + ": PROGRAMMER"