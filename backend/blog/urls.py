from django.urls import path
from . import views 
urlpatterns = [
    path('', views.PostListCreate.as_view(), name='post_list_create'),  # All post
    path('<str:author_id>/', views.PostListCreate.as_view(), name='post_list_create_by_author'),  # Post by author_id ( me=user, 1,2,3...= others)
    path('post/<int:pk>/delete/', views.DeletePost.as_view(), name='post-delete'),
    
    path('post/<int:post_id>/comments/', views.CommentListCreate.as_view(), name='comments_list_create'),
    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='comment-delete'),
    
    
    path('post/<int:content_id>/react/',views.ReactListCreate.as_view(),name='reactions_list_create'),
    path('react/<int:pk>/delete/', views.DeleteReact.as_view(), name='reaction-delete'),
]
