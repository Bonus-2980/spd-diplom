from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    text = models.TextField()
    image = models.ImageField(upload_to='posts/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Post(id={self.pk}, author={self.author_id})'


# для доп. задания
# class PostImage(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='posts/')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['id']


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                name='unique_like_per_user_post',
            ),
        ]
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Like(post={self.post_id}, user={self.user_id})'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return (
            f'Comment(id={self.pk}, post={self.post_id}, '
            f'author={self.author_id})'
        )

    def save(self, *args, **kwargs):
        if isinstance(self.text, bytes):
            self.text = self.text.decode('utf-8')
        super().save(*args, **kwargs)
