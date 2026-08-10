from django.shortcuts import render
from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
