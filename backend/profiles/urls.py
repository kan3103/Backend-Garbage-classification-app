from django.urls import path

from .views import UserListCreateView,ProfileDetailView

urlpatterns = [
    path('', UserListCreateView.as_view()),
    path('profile/<str:id>/',ProfileDetailView.as_view()),
]