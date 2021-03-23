# from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


User = get_user_model()



def create_user_account(email, password, name="", **extra_fields):
    user = User.objects.create_user(
        email=email, password=password, name=name, **extra_fields)
    return user


def get_and_authenticate_user(name, password, phone):
    user = authenticate(name=name, password=password, phone=phone)
    if user is None:
        raise serializers.ValidationError('invalid name/phone. please try again')
    return user