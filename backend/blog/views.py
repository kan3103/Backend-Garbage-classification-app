import json
from django.http import HttpResponse
from django.utils import timezone
from django.forms import ValidationError
from django.db.models import F
from .models import Comment,Post,Reaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny
from .serializers import PostSerializer,CommentSerializer,ReactionSerializer,UserSerializer
from rest_framework import generics
from rest_framework.exceptions import NotFound,PermissionDenied
from django.contrib.auth.models import User
# Create your views here.


#Handle Posts logic
class CustomJsonResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        kwargs['content_type'] = 'application/json; charset=utf-8'
        super().__init__(content=json.dumps(data, ensure_ascii=False), **kwargs)

class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        author_id = self.kwargs.get('author_id', None)

        if author_id == 'me':
            return Post.objects.filter(author=self.request.user).order_by('-updated_at')
        elif author_id:
            return Post.objects.filter(author_id=author_id).order_by('-updated_at')
        else:
            return Post.objects.all().order_by('-updated_at')

    def perform_create(self, serializer):
        author_id = self.kwargs.get('author_id', None)

        if author_id is not None and author_id != 'me':
            raise PermissionDenied("You do not have permission to create a post for another user.")

        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return CustomJsonResponse(response.data)

class DeletePost(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)

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
        post.updated_at=timezone.now()
        post.save()
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return CustomJsonResponse(response.data)

class DeleteComment(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(author = user)
        
#Handle Reacts logic
class ReactListCreate(generics.ListCreateAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        content_id = self.kwargs.get('content_id')
        status = self.request.query_params.get('status', None)      #Show list of people who like or dislike
        if status:
            return Reaction.objects.filter(content=content_id, reaction_type=status)
        return Reaction.objects.filter(content=content_id) #If none show all
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
        content.updated_at=timezone.now()
        content.save()
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return CustomJsonResponse(response.data)
    
class DeleteReact(generics.DestroyAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Reaction.objects.filter(author=user)

    def perform_destroy(self, instance):
        content_id = instance.content.id
        try:
            content = Post.objects.get(id=content_id)
        except Post.DoesNotExist:
            try:
                content = Comment.objects.get(id=content_id)
            except Comment.DoesNotExist:
                raise ValidationError('Content not found.')

        # Update the reaction 
        content.react = F('react') - 1
        content.save()
        instance.delete()

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]