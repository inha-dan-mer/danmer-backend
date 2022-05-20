from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import generics, status
# Create your views here.

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer