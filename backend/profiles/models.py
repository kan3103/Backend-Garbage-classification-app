from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    birthday = models.DateField()
    avatar = models.URLField()
    address = models.TextField()   