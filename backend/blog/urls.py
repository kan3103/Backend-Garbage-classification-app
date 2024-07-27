from django.urls import path
from . import views 
urlpatterns = [
    path('myblog',views.PostListCreate.as_view(), name="post_list_create"),
    path('myblog/delete/<int:pk>/', views.DeletePost.as_view(), name='post-delete'),
    
    path('<int:post_id>/comments/', views.CommentListCreate.as_view(), name='comments_list_create'),
    
    path('<int:content_id>/react/',views.ReactListCreate.as_view(),name='reactions_list_create')
]
