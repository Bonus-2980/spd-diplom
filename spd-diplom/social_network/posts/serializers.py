from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Post, Comment


User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'created_at')
        read_only_fields = ('author', 'created_at')

    def validate_text(self, value):
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        elif not isinstance(value, str):
            value = str(value)
        return value


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'text', 'image', 'created_at', 'comments', 'likes_count'
        )
        read_only_fields = ('created_at',)

    def get_likes_count(self, obj: Post) -> int:
        return obj.likes.count()

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return Post.objects.create(author=request.user, **validated_data)
        return super().create(validated_data)
