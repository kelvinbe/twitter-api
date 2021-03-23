from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

# Create your models here.


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        if not phone:
            raise ValueError("User must have a phone number")

        user = self.model(phone=phone, name=name, password=password)

        user.set_password(password)
        user.save()
        return user




class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)

    objects = UserAccountManager()

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = ["phone"]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.name + self.phone
