from django.contrib import admin

from core.models import Customer
from django.contrib.auth.admin import UserAdmin

admin.site.register(Customer, UserAdmin)
