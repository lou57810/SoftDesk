from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
# from .serializers import MyTokenObtainPairSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import RegisterSerializer
from rest_framework import generics
from django.views.generic import View
from django.contrib.auth import logout

"""
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

"""


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('/login')



