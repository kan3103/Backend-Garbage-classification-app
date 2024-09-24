from rest_framework import serializers
from .models import Post,Comment,Reaction
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.CharField(source='author.profile.avatar', read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    react_id = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['author_avatar','title', 'content', 'author', 'author_name', 'created_at', 'updated_at', 'react', 'id', 'like_count', 'dislike_count','comments','react_id',]
        extra_kwargs = {"author": {"read_only": True}}

    def get_like_count(self, obj):
        return Reaction.objects.filter(content=obj, reaction_type=1).count()

    def get_dislike_count(self, obj):
        return Reaction.objects.filter(content=obj, reaction_type=-1).count()
    
    def get_comments(self,obj):
        return Comment.objects.filter(post_id=obj).count()
    
    
    def get_react_id(self,obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if Reaction.objects.filter(content=obj, author=user).exists():
                return Reaction.objects.get(content= obj, author= user).id
            else: return 0
        return 0
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.CharField(source='author.profile.avatar', read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    react_id = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['author_avatar','content', 'author', 'author_name', 'created_at', 'updated_at', 'react', 'id', 'like_count', 'dislike_count','react_id']
        extra_kwargs = {"author":{"read_only":True}}
        
    def get_like_count(self, obj):
        return Reaction.objects.filter(content=obj, reaction_type=1).count()

    def get_dislike_count(self, obj):
        return Reaction.objects.filter(content=obj, reaction_type=-1).count()
    
    def get_react_id(self,obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if Reaction.objects.filter(content=obj, author=user).exists():
                return Reaction.objects.get(content= obj, author= user).id
            else: return 0
        return 0
    
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