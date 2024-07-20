from django.urls import path
from . import views 
urlpatterns = [
    path('/myblog',views.PostListCreate.as_view(), name="post_list"),
]
