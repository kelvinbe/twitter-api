from rest_framework import mixins, viewsets
from .serializers import UserRegisterSerializer, UserLoginSerializer, EmptySerializer
from .models import User
from .utils import create_user_account
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from rest_framework import status
from .utils import get_and_authenticate_user
from django.core.exceptions import ImproperlyConfigured
from . import serializers
from django.contrib.auth import get_user_model





# class UserViewSet(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     viewsets.GenericViewSet,
# ):
#     serializer_class = UserRegisterSerializer
#     queryset = User.objects.all()

User =  get_user_model()



class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = EmptySerializer
    queryset = User.objects.all()

    serializer_classes = {
        "login": UserLoginSerializer,
        "register": UserRegisterSerializer,
    }

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        print(user)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)
