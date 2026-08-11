from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view(), name='post_list_create_api'),
    path('posts/<int:pk>/', views.PostDetailAPIView.as_view(), name='post_detail_api'),
    path('posts/<int:post_id>/comments/', views.CommentListCreateAPIView.as_view(), name='comment_list_create_api'),
]