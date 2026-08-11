from rest_framework import serializers
from blog.models import Post

from comments.models import Comment

class PostSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only = True)
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'body', 'publish', 'status', 'tags']
        read_only_fields = ['author', 'slug', 'publish']
        validators = []

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'email', 'body', 'created', 'active']
        read_only_fields = ['created', 'active']