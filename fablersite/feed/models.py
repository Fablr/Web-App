from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey

class Following(models.Model):
    follower = models.ForeignKey(User, related_name='follower')
    following = models.ForeignKey(User, related_name='following')

    def __str__(self):
        return '{}, {}'.format(follower, following)

    class Meta:
        unique_together = ('follower', 'following')

EVENT_TYPE_CHOICES = (
    ('Listened', 'Listened'),
    ('Subscribe', 'Subscribed'),
    ('Commented', 'Commented'),
    ('Followed', 'Followed'),
)

class Event(models.Model):
    user = models.ForeignKey(User, related_name='user')
    posted_time = models.DateTimeField(default=timezone.now)
    event_type = models.CharField(choices=EVENT_TYPE_CHOICES, max_length=50)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    event_object = GenericForeignKey('content_type', 'object_id')
    info = JSONField()

    def __str__(self):
        return '{} @ {} by {} for {}.{}'.format(event_type, posted_time, user, model_type, model_id)
