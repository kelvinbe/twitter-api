from django.shortcuts import render
from rest_framework import serializers
# from .models import User
from django.contrib.auth import password_validation, get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


# Create your views here.

User =  get_user_model()


class UserLoginSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300, required=True)
    phone = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(required=True, write_only=True)




class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ('name', 'phone', 'email', 'auth_token')
        read_only_fields = ('is_active', 'is_staff')

    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'phone', 'password', 'email')


    def create(self, validated_data):
        user = User.objects.create_user(validated_data['name'], validated_data['phone'], validated_data['password'], validated_data['email'])

        return user


class EmptySerializer(serializers.Serializer):
    pass

    


























