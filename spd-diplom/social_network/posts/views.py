from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return False


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.all()
        .select_related('author')
        .prefetch_related('comments', 'likes')
    )
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save()

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def like(self, request, pk=None):
        post = self.get_object()
        Like.objects.get_or_create(post=post, user=request.user)
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def unlike(self, request, pk=None):
        post = self.get_object()
        Like.objects.filter(post=post, user=request.user).delete()
        return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def comment(self, request, pk=None):
        post = self.get_object()

        text = request.data.get('text', '')

        if isinstance(text, bytes):
            try:
                text = text.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text = text.decode('cp1251')
                except UnicodeDecodeError:
                    text = text.decode('cp866', errors='ignore')

        Comment.objects.create(
            post=post,
            author=request.user,
            text=text,
        )

        return Response({'status': 'commented'}, status=status.HTTP_201_CREATED)
