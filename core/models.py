from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from store.models import CartItem
from django.contrib.auth.models import AbstractBaseUser
from enum import IntEnum
from django_countries.fields import CountryField

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class AuthLevel(IntEnum):
    VOID = 0
    Customer = 1
    Worker = 2
    Admin = 3
    Programmer = 4


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


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


class Customer(AbstractBaseUser):
    email = models.EmailField()
    address_info = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    cart = models.ManyToManyField(CartItem) #on_delete=models.CASCADE)
    auth_level = AuthLevel.Customer

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username = models.CharField(max_length=100, unique=True)
    auth_level = models.IntegerField(default=AuthLevel.Customer)
    desc = models.CharField(max_length=100, unique=False, default="Please enter a description.")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.user.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Worker(models.Model):
    auth_level = AuthLevel.Worker


class Owner(models.Model):
    auth_level = AuthLevel.Admin


class Programmer(Owner):
    auth_level = AuthLevel.Programmer

    def __str__(self):
        return self.user.username + ": PROGRAMMER"