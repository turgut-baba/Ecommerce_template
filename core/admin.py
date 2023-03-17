from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomerCreationForm, CustomerChangeForm
from .models import Programmer

# TODO: Change this to be inside the admin in the models file.
class CustomUserAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Programmer
    list_display = ["email", "username"]

# admin.site.register(Programmer, CustomUserAdmin)