from rest_framework import serializers
from .models import Post,Comment,Reaction
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'author_name', 'created_at', 'updated_at', 'react', 'id', 'like_count', 'dislike_count','comments']
        extra_kwargs = {"author": {"read_only": True}}

    def get_like_count(self, obj):
        return Reaction.objects.filter(content=obj, reaction_type=1).count()

    def get_dislike_count(self, obj):
        return Reaction.objects.filter(content=obj, reaction_type=-1).count()
    
    def get_comments(self,obj):
        return Comment.objects.filter(post_id=obj).count()

        
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['content', 'author', 'author_name', 'created_at', 'updated_at', 'react', 'id', 'like_count', 'dislike_count']
        extra_kwargs = {"author":{"read_only":True}}
        
    def get_like_count(self, obj):
        return Reaction.objects.filter(content=obj, reaction_type=1).count()

    def get_dislike_count(self, obj):
        return Reaction.objects.filter(content=obj, reaction_type=-1).count()
        
class ReactionSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
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