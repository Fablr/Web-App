from rest_framework import generics, viewsets, permissions
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from podcast.models import Podcast, Publisher, Episode
from podcast.serializers import *
from authentication.permissions import IsStaffOrTargetUser

class PublisherDetailView(generic.DetailView):
    model = Publisher
    def get_context_data(self, *args, **kwargs):
        context = super(PublisherDetailView, self).get_context_data(*args, **kwargs)
        context['podcast_list'] = Podcast.objects.filter(publisher=self.kwargs['pk'])
        return context

class PodcastDetailView(generic.DetailView):
    model = Podcast
    def get_context_data(self, *args, **kwargs):
        context = super(PodcastDetailView, self).get_context_data(*args, **kwargs)
        context['episode_list'] = Episode.objects.filter(podcast=self.kwargs['pk'])
        return context



# Django Rest API
# ViewSets define the view behavior.
class PodcastViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated]
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (permissions.AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),


class PublisherViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    #required_scopes = ['groups']
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (permissions.AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class EpisodeViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (permissions.AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),


    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
