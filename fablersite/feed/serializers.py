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
        fields = ('id', 'user', 'posted_time', 'event_type', 'event_object', 'info')

class FeedSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    event_object = GenericRelatedField({
        Podcast: PodcastSerializer(),
        Episode: EpisodeSerializer(),
        Comment: CommentViewSerializer(),
        UserProfile: UserProfileSerializer(),
    })

    def get_user(self, event):
        user_profile = UserProfile.objects.get(pk=event.user.pk)
        request = self.context.get('request', None)
        profile_serializer = UserProfileSerializer(user_profile, context={'request': request})
        return profile_serializer.data

    class Meta:
        model = Event
        fields = ('id', 'user', 'posted_time', 'event_type', 'event_object', 'info')
