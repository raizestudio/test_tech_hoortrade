from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import BaseUserTokenSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = BaseUserTokenSerializer
