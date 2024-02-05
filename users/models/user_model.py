from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise TypeError(_("email field is required"))

        if not password:
            raise TypeError(_("email field is required"))

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        full_name = input("Enter full name:").title()
        gender = input("Enter gender (male/female): ").lower()
        while gender not in ['male', 'female']:
            print("Invalid gender. Please enter 'male', 'female'")
            gender = input("Enter gender (male/female): ").lower()

        profile = {
            "full_name": full_name,
            "gender": gender
        }
        from users.signals import profile_values
        profile_values.send(sender=User, user=user, profile=profile)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken().for_user(self)
        return {
            "refresh": str(refresh),
            "access_token": str(refresh.access_token)
        }
