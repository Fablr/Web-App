from rest_framework import generics, viewsets, permissions
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from podcast.models import Podcast, Publisher, Episode
from threadedcomments.models import ThreadedComment
from podcast.serializers import *
from authentication.permissions import IsStaffOrTargetUser
import django_filters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics, status

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

#class CommentViewSet(viewsets.ModelViewSet):
#    queryset = ThreadedComment.objects.exclude(parent__isnull=False)
#    serializer_class = EpisodeCommentSerializer

class EpisodeCommentsList(APIView):
    def get_object(self, pk):
        try: 
            return ThreadedComment.objects.all()
        except ThreadedComment.DoesNotExist:
            raise Http404
    def get(self, request, format=None):
        comments = ThreadedComment.objects.all()
        serializer = EpisodeCommentSerializer(comments, many=True)
        return Response(serializer.data)


class EpisodeCommentsDetail(APIView):
    def get_object(self, pk):
        try: 
            return ThreadedComment.objects.filter(object_pk=pk)
        except ThreadedComment.DoesNotExist:
            raise Http404
    def get(self, request, pk=None, format=None):
        if pk is None:
            comments = ThreadedComment.objects.all()
            serializer = EpisodeCommentThreadSerializer(comments, many=True)
            return Response(serializer.data)            
        else:
            comments = ThreadedComment.objects.filter(object_pk=pk)
            serializer = EpisodeCommentThreadSerializer(comments, many=True)
            return Response(serializer.data)

    def post(self, request, pk=None, format=None):
        serializer = EpisodeCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

