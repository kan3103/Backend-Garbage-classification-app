from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.
class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()