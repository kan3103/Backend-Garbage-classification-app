from django.urls import path
from . import views 
urlpatterns = [
    path('myblog',views.PostListCreate.as_view(), name="post_list"),
    path('<int:post_id>/comments/', views.CommentListCreate.as_view(), name='choice_list_create'),
]
