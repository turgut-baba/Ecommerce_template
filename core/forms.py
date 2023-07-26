from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Customer, Address, ADDRESS_CHOICES
from django_countries.data import COUNTRIES


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AddressForm(forms.Form):
    title = forms.CharField(max_length=20)
    address_long = forms.CharField(max_length=500)

    apartment_no = forms.CharField(max_length=100)
    apartment_floor = forms.CharField(max_length=10)
    apartment_flat = forms.CharField(max_length=10)

    country = forms.ChoiceField(choices=COUNTRIES.items())
    zip = forms.CharField(max_length=100)
    address_type = forms.CharField(max_length=1)
    # default = forms.BooleanField()

    class Meta:
        model = Address
        fields = ['title', 'address_type', 'address_long', 'apartment_no', 'apartment_floor', 'apartment_flat', 'country', 'zip']

    def save(self, commit=True):
        address = Address.objects.create()
        address.title = self.cleaned_data['title']
        address.address_long = self.cleaned_data['address_long']
        address.apartment_no = self.cleaned_data['apartment_no']
        address.apartment_floor = self.cleaned_data['apartment_floor']
        address.apartment_flat = self.cleaned_data['apartment_flat']
        address.country = self.cleaned_data['country']
        address.title = self.cleaned_data['title']
        address.zip = self.cleaned_data['zip']
        address.address_type = self.cleaned_data['address_type']
        address.default = True

        if commit:
            address.save()

        return address

