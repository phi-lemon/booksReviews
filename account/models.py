from django.db import models
from django.conf import settings


class UserFollows(models.Model):
    """
    This table stores relations between followed_user_id and user_id
    Referencing 'auth.User' VS settings.AUTH_USER_MODEL:
    see https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#referencing-the-user-model
    settings.AUTH_USER_MODEL will return the currently active user model:
    the custom user model if one is specified, or User otherwise.
    If AUTH_USER_MODEL is not defined in settings, settings.AUTH_USER_MODEL is equivalent to 'auth.User'
    WARNING Changing AUTH_USER_MODEL after you’ve created database tables is significantly more difficult since
    it affects foreign keys and many-to-many relationships, for example.
    The model referenced by AUTH_USER_MODEL must be created before the first migration of its app
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followed_by', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)
        ordering = ('-date_created',)

    def __str__(self):
        return f'{self.user} -> {self.followed_user}'

