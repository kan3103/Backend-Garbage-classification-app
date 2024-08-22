from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import TokenSerializer
from django.contrib.auth.models import User
from .models import VerificationCode
from django.core.mail import send_mail
from django.conf import settings
import requests

# Create your views here.
class GoogleLogin(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer
    def get(self, request):
        access_token = request.GET.get('access_token')
        print(access_token)
        data = requests.get(f"https://www.googleapis.com/oauth2/v2/userinfo", headers={
            "Authorization": f"Bearer {access_token}"
        }).json()
        user =  User.objects.get_or_create(username=data['email'])[0]
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        serializer = TokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        json = JSONRenderer().render(serializer.data)
        return HttpResponse(json, status=200)