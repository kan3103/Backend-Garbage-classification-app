from django.forms import ValidationError
from django.db.models import F
from django.shortcuts import render
from .models import Comment,Post,Reaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny
from .serializers import PostSerializer,CommentSerializer,ReactionSerializer,UserSerializer
from rest_framework import generics
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User
# Create your views here.


#Handle Posts logic
class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class DeletePost(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author = user)

#Handle Comments logic
class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound('Post not found')
        serializer.save(author=self.request.user, post_id=post)
        
        
#Handle Reacts logic
class ReactListCreate(generics.ListCreateAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        content_id = self.kwargs.get('content_id')
        return Reaction.objects.filter(content=content_id)

    def perform_create(self, serializer):
        content_id = self.kwargs.get('content_id')
        content = None
        user = self.request.user
        try:
            content = Post.objects.get(id=content_id)
        except Post.DoesNotExist:
            try:
                content = Comment.objects.get(id=content_id)
            except Comment.DoesNotExist:
                raise ValidationError('Content not found.')


        if Reaction.objects.filter(author=user, content=content).exists():
            raise ValidationError('You have already liked this content.')


        serializer.save(author=user, content=content)
        content.react = F('react') + 1
        content.save()


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]