from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework_recursive.fields import RecursiveField
from podcast.models import Podcast, Episode, Publisher, Subscription, EpisodeReceipt

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import *
from django.utils.duration import duration_string

import datetime

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


#class VoteSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Vote
#        fields = ('value', 'comment')


#class EpisodeCommentThreadSerializer(serializers.ModelSerializer):
    #parent = RecursiveField(allow_null=True, many=True)
#    username = serializers.SerializerMethodField()
#    uservote = serializers.SerializerMethodField()
#    class Meta:
#        model = ThreadedComment
#        fields = ('id', 'comment', 'user', 'submit_date', 'parent', 'username', 'is_removed', 'vote_weight', 'uservote')

#    def get_username(self, obj):
#        return obj.user.username
#
#    def get_uservote(self, obj):
#        try:
#            return Vote.objects.get(comment=obj.id, voter_user=obj.user).value
#        except Vote.DoesNotExist:
#            return 0


#class EpisodeCommentSerializer(serializers.ModelSerializer):
    #parent = RecursiveField(allow_null=True, many=True)
#    class Meta:
#        model = ThreadedComment
#        fields = ('comment', 'parent')

#    def create(self, validated_data):
#        ctype = ContentType.objects.get_by_natural_key('podcast', 'episode')
#        validated_data['content_type'] = ctype
#        validated_data['site_id'] = settings.SITE_ID
#        return ThreadedComment.objects.create(**validated_data)

#class EpisodeCommentUpdateSerializer

#class EpisodeVoteSerializer(serializers.ModelSerializer):
    #class Meta:
        #model =
