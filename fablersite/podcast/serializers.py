from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework_recursive.fields import RecursiveField
from podcast.models import Podcast, Episode, Publisher, Subscription

from django.contrib.contenttypes.models import ContentType
from django.conf import settings

# first we define the serializers
class PublisherSerializer(serializers.ModelSerializer):
    podcast = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='podcast-detail')
    class Meta:
        model = Publisher

class PodcastSerializer(serializers.ModelSerializer):
    #publisher = serializers.HyperlinkedRelatedField(read_only=True, view_name='publisher-detail')
    episode = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='episode-detail')
    class Meta:
        model = Podcast


class EpisodeSerializer(serializers.ModelSerializer):
    #podcast = serializers.HyperlinkedRelatedField(read_only=True, view_name='podcast-detail')
    #publisher = serializers.HyperlinkedRelatedField(read_only=True, view_name='publisher-detail')
    class Meta:
        model = Episode


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription

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
