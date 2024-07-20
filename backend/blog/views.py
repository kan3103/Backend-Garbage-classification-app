from django.shortcuts import render
from .models import Comment,Post,Reaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny
from .serializers import PostSerializer,CommentSerializer,ReactionSerializer,UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
# Create your views here.

class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author = user)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]