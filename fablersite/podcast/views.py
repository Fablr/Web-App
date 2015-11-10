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

from rest_framework.decorators import api_view, list_route
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics, status
from rest_framework.reverse import reverse

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


class PodcastViewSet(viewsets.ModelViewSet):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    filter_class = PodcastFilter

    """
    Retrieve subscribed podcasts for current user.
    """
    @list_route()
    def subscribed(self, serializer):
        podcasts = [x.podcast for x in Subscription.objects.filter(user=self.request.user, active=True)]
        serializer = PodcastSerializer(podcasts, many=True, context={'request': self.request})
        return Response(serializer.data)


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
    lookup_field = 'podcast'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        if 'user' in self.request.data:
            user = User.objects.get(id=request.data['user'])
        else:
            user = self.request.user

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg], 'user': user}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        assert 'podcast' in request.data, (
            'Missing Podcast field in requests data.'
        )

        try:
            if 'user' in request.data:
                user = User.objects.get(id=request.data['user'])
            else:
                user = self.request.user
            podcast = Podcast.objects.get(id=request.data['podcast'])
            instance, created = Subscription.objects.get_or_create(podcast=podcast, user=user)
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            if created:
                op = status.HTTP_201_CREATED
            else:
                op = status.HTTP_200_OK
            return Response(serializer.data, status=op, headers=headers)
        except ObjectDoesNotExist:
            raise Http404


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
