from rest_framework import serializers
from .models import Post,Comment,Reaction
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {"author":{"read_only":True}}
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {"author":{"read_only":True}}
        
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
        extra_kwargs = {"author":{"read_only":True}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','id','password']
        extra_kwargs = {"password":{"write_only":True}}
    
    def create(self, validated_date):
        user = User.objects.create_user(**validated_date)
        return user