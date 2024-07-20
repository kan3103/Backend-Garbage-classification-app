from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    react = models.IntegerField(auto_created=0)

class Post (TimeStampedModel,Blog):
    title = models.CharField(max_length=100)
    content = models.TextField()

class Comment(TimeStampedModel,Blog):
    content = models.CharField(max_length=200)


class Reaction(TimeStampedModel):
    REACTION_CHOICES = [
        (1, 'Like'),
        (-1, 'Dislike'),
    ]
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    reaction_type = models.IntegerField(choices=REACTION_CHOICES)
    # react = models.BooleanField()

