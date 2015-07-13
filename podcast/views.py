from django.shortcuts import render
from rest_framework import generics, viewsets, permissions

from podcast.models import Podcast, Publisher, Episode
from podcast.serializers import *
# Django Rest API
# ViewSets define the view behavior.
class PodcastViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    permission_classes = [permissions.IsAuthenticated]
    required_scopes = ['groups']
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class EpisodeViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer

