import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.duration import duration_string
from rest_framework import serializers

from podcast.models import Podcast, Episode, Publisher, Subscription, EpisodeReceipt

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher

class PodcastSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()
    publisherName = serializers.SerializerMethodField()

    def get_subscribed(self, podcast):
        subscribed = False
        request = self.context.get('request', None)
        if request is not None:
            try:
                if request.user.is_authenticated():
                    subscription = Subscription.objects.get(podcast=podcast.pk, user=request.user)
                    subscribed = subscription.active
            except ObjectDoesNotExist:
                pass
        return subscribed

    def get_publisherName(self, podcast):
        return podcast.publisher.name

    class Meta:
        model = Podcast

class EpisodeSerializer(serializers.ModelSerializer):
    mark = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    def get_mark(self, episode):
        mark = duration_string(datetime.timedelta(seconds=0))
        request = self.context.get('request', None)
        if request is not None:
            try:
                if request.user.is_authenticated():
                    receipt = EpisodeReceipt.objects.get(episode=episode.pk, user=request.user)
                    mark = duration_string(receipt.mark)
            except ObjectDoesNotExist:
                pass
        return mark

    def get_completed(self, episode):
        completed = False
        request = self.context.get('request', None)
        if request is not None:
            try:
                if request.user.is_authenticated():
                    receipt = EpisodeReceipt.objects.get(episode=episode.pk, user=request.user)
                    completed = receipt.completed
            except ObjectDoesNotExist:
                pass
        return completed

    class Meta:
        model = Episode


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ('podcast', 'user', 'active')

class EpisodeReceiptSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = EpisodeReceipt
