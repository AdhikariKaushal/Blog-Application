from django.shortcuts import render
from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer

class PostListAPIView(generics.ListAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
