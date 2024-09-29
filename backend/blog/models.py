from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class ContentModel(TimeStampedModel):
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    # picture = models.ImageField(upload_to='', null=True, blank=True)


    
class Post (ContentModel):
    title = models.CharField(max_length=100)
    content = models.TextField()

class Comment(ContentModel):
    content = models.CharField(max_length=200)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)


class Reaction(TimeStampedModel):
    class ReactionType(models.IntegerChoices):
        LIKE = 1, 'Like'
        DISLIKE = -1, 'Dislike'
        
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.IntegerField(choices=ReactionType.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'content'],
                name='unique_reaction_content'
            ),
        ]

