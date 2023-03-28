from django.shortcuts import get_object_or_404
from .models import Customer
import logging
from django.contrib.auth.backends import BaseBackend


class AuthCustomer(BaseBackend):
    def authenticate(self, request, name=None, password=None):
        try:
            user = get_object_or_404(Customer, name=name)
            if user.check_password(password):
                return user
            else:
                return None
        except Customer.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists ")
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, user_id):
        try:
            user = Customer.objects.get(id=user_id)
            if user.is_active:
                return user
            return None
        except Customer.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None