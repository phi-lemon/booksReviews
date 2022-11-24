from django.db import models
from django.contrib.auth import get_user_model


class UserFollows(models.Model):
    user = models.ForeignKey('auth.User', related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey('auth.User', related_name='followed_by', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} follows {self.followed_user}'


# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('follows',
                        models.ManyToManyField('self',
                                               through=UserFollows,
                                               related_name='followers',
                                               symmetrical=False))
