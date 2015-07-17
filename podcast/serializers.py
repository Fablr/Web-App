from rest_framework import serializers
from django.contrib.auth.models import User, Group
from podcast.models import Podcast, Episode, Publisher

# first we define the serializers
class PublisherSerializer(serializers.ModelSerializer):
    podcast = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='podcast-detail')
    class Meta:
        model = Publisher

class PodcastSerializer(serializers.ModelSerializer):
    publisher = serializers.HyperlinkedRelatedField(read_only=True, view_name='publisher-detail') 
    episode = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='episode-detail')
    class Meta:
        model = Podcast

class EpisodeSerializer(serializers.ModelSerializer):
    podcast = serializers.HyperlinkedRelatedField(read_only=True, view_name='podcast-detail') 
    publisher = serializers.HyperlinkedRelatedField(read_only=True, view_name='publisher-detail')     
    class Meta:
        model = Episode
