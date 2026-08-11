from django.shortcuts import render
from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.text import slugify
from rest_framework.exceptions import PermissionDenied
from comments.models import Comment
from .serializers import CommentSerializer

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        serializer.save(author = self.request.user, slug = slugify(title))

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("Your are not allowed to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You are not allowed to delete this post.")
        instance.delete()

class CommentListCreateAPIView (generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, active = True)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(post_id=post_id)