from django.db import models
from django.contrib.auth import get_user_model


class UserFollows(models.Model):
    # voir https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#referencing-the-user-model
    user = models.ForeignKey('auth.User', related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey('auth.User', related_name='followed_by', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)
        ordering = ('-date_created',)

    def __str__(self):
        return f'{self.user} -> {self.followed_user}'

