from django.contrib.auth.models import User
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from authentication.models import UserProfile
from authentication.serializers import UserProfileSerializer
from feed.models import Following, Event
from podcast.models import Podcast, Episode
from podcast.serializers import PodcastSerializer, EpisodeSerializer
from threaded_comments.models import Comment
from threaded_comments.serializers import CommentViewSerializer


class FollowingSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Following


class EventSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    event_object = GenericRelatedField({
        Podcast: PodcastSerializer(),
        Episode: EpisodeSerializer(),
        Comment: CommentViewSerializer(),
        UserProfile: UserProfileSerializer(),
    })

    class Meta:
        model = Event
        fields = ('user', 'posted_time', 'event_type', 'event_object', 'info')
