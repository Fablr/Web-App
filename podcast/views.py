from rest_framework import generics, viewsets, permissions
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from podcast.models import Podcast, Publisher, Episode
from podcast.serializers import *
from authentication.permissions import IsStaffOrTargetUser
import django_filters

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

class EpisodeDetailView(generic.DetailView):
    model = Episode

class PublisherFilter(django_filters.FilterSet):
    class Meta:
        model = Publisher

class PodcastFilter(django_filters.FilterSet):
    class Meta:
        model = Podcast

class EpisodeFilter(django_filters.FilterSet):
    class Meta:
        model = Episode

# Django Rest API
# ViewSets define the view behavior.
class PodcastViewSet(viewsets.ModelViewSet):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    filter_class = PodcastFilter


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filter_class = PublisherFilter

class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_class = EpisodeFilter

