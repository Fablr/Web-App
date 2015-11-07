from rest_framework import generics, viewsets, permissions
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from podcast.models import Podcast, Publisher, Episode, Subscription
from podcast.serializers import *
from authentication.permissions import IsStaffOrTargetUser
import django_filters

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics, status
from rest_framework.reverse import reverse

@api_view(['GET'])
def current_subscriptions(request):
    """
    Returns Podcasts the current user is subscribed to.
    """
    podcasts = Podcast.objects.filter(pk__in = [x.podcast.pk for x in Subscription.objects.filter(user=request.user)])
    serializer = PodcastSerializer(podcasts, many=True, context={'request': request})
    return Response(serializer.data)

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

class SubscriptionDetailView(generic.DetailView):
    model = Subscription

class PublisherFilter(django_filters.FilterSet):
    class Meta:
        model = Publisher

class PodcastFilter(django_filters.FilterSet):
    class Meta:
        model = Podcast

class EpisodeFilter(django_filters.FilterSet):
    class Meta:
        model = Episode
        fields = ['podcast']

class SubscriptionFilter(django_filters.FilterSet):
    class Meta:
        model=Subscription
        fields = ['podcast', 'user']

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


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    filter_class = SubscriptionFilter


#class CommentViewSet(viewsets.ModelViewSet):
#    queryset = ThreadedComment.objects.exclude(parent__isnull=False)
#    serializer_class = EpisodeCommentSerializer

#class VoteDetail(APIView):
#    def get(self, request, pk=None, format=None):
#        if pk is None:
#            votes = Vote.objects.all()
#            serializer = VoteSerializer(votes, many=True)
#            return Response(serializer.data)
#        else:
#            votes = Vote.objects.get(id=pk)
#            serializer = VoteSerializer(votes, many=True)
#            return Response(serializer.data)
#
#    def post(self, request, format=None):
#        serializer = VoteSerializer(data=request.data)
#        if serializer.is_valid():
#            # Using episode id, update comment's vote weight
#            comment_id = ThreadedComment.objects.get(pk=request.data['comment'])
#            # If vote already exists update existing vote to reflect new value
#            try:
#                vote = Vote.objects.get(comment=comment_id, voter_user=request.user)
#                comment_id.vote_weight = comment_id.vote_weight - vote.value
#                vote.value = int(request.data['value'])
#                if vote.value == 0:
#                    vote.delete()
#                else:
#                    vote.save()
#            except Vote.DoesNotExist:
#                vote = serializer.save(voter_user=request.user, voted_user=comment_id.user, vote_time=timezone.now())
#            comment_id.vote_weight = comment_id.vote_weight + int(request.data['value'])
#            comment_id.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#
#
#class EpisodeThreadList(APIView):
#    def get_object(self, pk):
#        try:
#            return ThreadedComment.objects.all()
#        except ThreadedComment.DoesNotExist:
#            raise Http404
#    def get(self, request, pk=None, format=None):
#        if pk is None:
#            comments = ThreadedComment.objects.all()
#            serializer = EpisodeCommentThreadSerializer(comments, many=True)
#            return Response(serializer.data)
#        else:
#            comments = ThreadedComment.objects.filter(object_pk=pk)
#            serializer = EpisodeCommentThreadSerializer(comments, many=True)
#            return Response(serializer.data)
#
#
#class EpisodeCommentsDetail(APIView):
#    def get_object(self, pk):
#        try:
#            return ThreadedComment.objects.filter(object_pk=pk)
#        except ThreadedComment.DoesNotExist:
#            raise Http404
#    def get(self, request, pk=None, format=None):
#        if pk is None:
#            comments = ThreadedComment.objects.all()
#            serializer = EpisodeCommentThreadSerializer(comments, many=True)
#            return Response(serializer.data)
#        else:
#            comments = ThreadedComment.objects.get(id=pk)
#            serializer = EpisodeCommentThreadSerializer(comments, many=True)
#            return Response(serializer.data)
#
#    def post(self, request, pk, format=None):
#        serializer = EpisodeCommentSerializer(data=request.data)
#        if serializer.is_valid():
#            # Create a comment, then create a corresponding vote
#            comment = serializer.save(user=request.user, object_pk=pk, submit_date=timezone.now(), ip_address=request.META['REMOTE_ADDR'], vote_weight=1)
#            vote = Vote(voter_user=request.user, voted_user=request.user, comment=comment, value=1, vote_time=timezone.now())
#            vote.save()
#            serializer = EpisodeCommentThreadSerializer(comment)
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk):
#        comment = ThreadedComment.objects.get(pk=pk)
#        comment.delete()
#        queryset = Vote.objects.filter(comment_id=pk)
#        queryset.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

    #def update(self, request, pk):
        #comment =
