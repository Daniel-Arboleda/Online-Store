from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from Lucky.models import CustomUser, User


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
            print(f"Email '{username}' exists in Auth table: True")
            if user.check_password(password):
                return user
            else:
                print(f"Password for '{username}' is incorrect.")
        except CustomUser.DoesNotExist:
            print(f"Email '{username}' does not exist in Auth table.")
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None