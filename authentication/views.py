from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import MyTokenObtainPairSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import RegisterSerializer
from rest_framework import generics

"""
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

"""
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

