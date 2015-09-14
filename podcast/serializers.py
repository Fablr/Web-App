from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework_recursive.fields import RecursiveField
from podcast.models import Podcast, Episode, Publisher
from threadedcomments.models import ThreadedComment



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

class EpisodeCommentThreadSerializer(serializers.ModelSerializer):
    #parent = RecursiveField(allow_null=True, many=True)
    username = serializers.SerializerMethodField()
    class Meta:
        model = ThreadedComment
        fields = ('id', 'comment', 'user', 'submit_date', 'parent', 'username')

    def get_username(self, obj):
        return obj.user.username

class EpisodeCommentSerializer(serializers.ModelSerializer):
    #parent = RecursiveField(allow_null=True, many=True)
    class Meta:
        model = ThreadedComment
        fields = ('comment', 'user', 'submit_date', 'parent', 'ip_address')

    def create(self, validated_data):
        return ThreadedComment(**validated_data)

    #def update(self, validated_data):


