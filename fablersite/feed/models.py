from django.db import models
from django.contrib.auth.models import User

class Following(models.Model):
    follower = models.ForeignKey(User, related_name='follower')
    following = models.ForeignKey(User, related_name='following')

    def __str__(self):
        return '{}, {}'.format(follower, following)

    class Meta:
        unique_together = ('follower', 'following')
