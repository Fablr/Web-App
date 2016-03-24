from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import transaction
from django.db import models
from django.utils import timezone

from authentication.models import UserProfile


class Following(models.Model):
    follower = models.ForeignKey(User, related_name='follower')
    following = models.ForeignKey(User, related_name='following')

    def __str__(self):
        return '{}, {}'.format(self.follower, self.following)

    class Meta:
        unique_together = ('follower', 'following')

    @transaction.atomic
    def save(self, *args, **kwargs):
        log_event = not self.pk

        super(Following, self).save(*args, **kwargs)

        if log_event:
            following_profile = UserProfile.objects.get(pk=self.following.pk)
            ctype = ContentType.objects.get_for_model(following_profile)
            event = Event.objects.create(user=self.follower, event_type='Followed', content_type=ctype, object_id=following_profile.pk)


EVENT_TYPE_CHOICES = (
    ('Listened', 'Listened'),
    ('Subscribed', 'Subscribed'),
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
    info = JSONField(default=dict)

    def __str__(self):
        return '{} @ {} by {} for {}.{}'.format(event_type, posted_time, user, content_type, object_id)
