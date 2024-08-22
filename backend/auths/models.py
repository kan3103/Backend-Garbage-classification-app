from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

# Create your models here.
class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expired_at = models.DateTimeField()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.code = ''.join(random.choices(string.digits, k=6))
        self.expired_at = timezone.now() + timezone.timedelta(minutes=5)
        super(VerificationCode, self).save(*args, **kwargs)

    def validate(self, code):
        return self.code == code and self.expired_at > timezone.now()