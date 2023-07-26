from django.contrib import admin

from core.models import Customer, Address
from django.contrib.auth.admin import UserAdmin


admin.site.register(Customer)
