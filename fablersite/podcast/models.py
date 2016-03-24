from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from durationfield.db.models.fields.duration import DurationField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from threaded_comments.models import Comment
from django.utils import timezone

from feed.models import *


class Publisher(models.Model):
    """
    Model for each Publisher of Podcasts
    """
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=255, blank=True, unique=True)
    users = models.ManyToManyField(User, blank=True)
    image = models.URLField(max_length=255, blank=True, default='')
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.name


class Podcast(models.Model):
    """
    Model for each podcast
    """
    publisher = models.ForeignKey(Publisher, related_name='podcast')
    title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    summary = models.TextField(max_length=4000, blank=True)
    category = models.CharField(max_length=255, blank=True)
    explicit = models.BooleanField(default=False)
    link = models.URLField(max_length=255, blank=True)
    image = models.URLField(max_length=255, blank=True, default='')
    language = models.CharField(max_length=255, blank=True)
    copyright = models.CharField(max_length=255, blank=True)
    blocked = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    keywords = models.CharField(max_length=100, blank=True)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title


class Episode(models.Model):
    """
    Model for episodes of Podcasts
    """
    podcast = models.ForeignKey(Podcast, related_name='episode')
    title = models.CharField(max_length=255, blank=True)
    link = models.URLField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=4000, blank=True)
    blocked = models.BooleanField(default=False)
    pubdate = models.DateTimeField(null=False, blank=True, default=timezone.now)
    duration = models.DurationField(null=False, blank=True, default='0d 0:00:02')
    keywords = models.CharField(max_length=100, blank=True)
    explicit = models.BooleanField(default=False)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """
    Model for Subscription to Podcasts by Users
    """
    podcast = models.ForeignKey(Podcast, related_name='subscriptionPodcast')
    user = models.ForeignKey(User, related_name='subscriptionUser')
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}, {}: {}'.format(podcast, user, active)

    class Meta:
        unique_together = ('podcast', 'user',)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.active:
            event = Event.objects.get_or_create(user=self.user, event_type='Subscribed', event_object=self.podcast)
            event.save()
        super(Episode, self).save(*args, **kwargs)

class EpisodeReceipt(models.Model):
    """
    Model for listening state of Episodes by Users
    """
    episode = models.ForeignKey(Episode, related_name='receiptEpisode')
    user = models.ForeignKey(User, related_name='receiptUser')
    mark = models.DurationField(null=False, blank=True, default='0d 0:00:02')
    completed = models.BooleanField(null=False, blank=True, default=False)

    def __str__(self):
        return '{}, {}: {}, {}'.format(episode, user, time, completed)

    class Meta:
        unique_together = ('episode', 'user',)


# class EpisodeTimeline(models.Model)


# class EpisodeDiscussion(models.Model)
