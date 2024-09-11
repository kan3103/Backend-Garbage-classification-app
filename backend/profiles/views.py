from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserSerializer,ProfileSerializer
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileDetailView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        author_id = self.kwargs.get('id', None)
        
        if author_id == "me":
            user = self.request.user
            profile = Profile.objects.filter(user=user).first()
        else:
            profile = Profile.objects.filter(user=author_id).first()

        if profile is None:
            return Response("Page not found", status=404)
        
        
        serializer = ProfileSerializer(instance=profile)
        return Response(serializer.data, content_type='application/json; charset=utf-8')