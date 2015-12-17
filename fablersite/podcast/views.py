from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from podcast.models import Podcast, Publisher, Episode, Subscription, EpisodeReceipt
from podcast.serializers import *
from podcast.mixins import *

from authentication.permissions import IsStaffOrTargetUser

import django_filters

from rest_framework.decorators import api_view, list_route
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics, status, viewsets
from rest_framework.reverse import reverse

class PublisherFilter(django_filters.FilterSet):
    class Meta:
        model = Publisher


class PodcastFilter(django_filters.FilterSet):
    class Meta:
        model = Podcast
        fields = ['publisher']


class EpisodeFilter(django_filters.FilterSet):
    class Meta:
        model = Episode
        fields = ['podcast']


class SubscriptionFilter(django_filters.FilterSet):
    class Meta:
        model=Subscription
        fields = ['podcast', 'user']


class EpisodeReceiptFilter(django_filters.FilterSet):
    class Meta:
        model=EpisodeReceipt
        fields = ['episode', 'user']


class PodcastViewSet(viewsets.ModelViewSet, CommentMixin):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    filter_class = PodcastFilter

    @list_route()
    def subscribed(self, serializer):
        podcasts = [x.podcast for x in Subscription.objects.filter(user=self.request.user, active=True)]
        serializer = PodcastSerializer(podcasts, many=True, context={'request': self.request})
        return Response(serializer.data)


class PublisherViewSet(viewsets.ModelViewSet, CommentMixin):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filter_class = PublisherFilter


class EpisodeViewSet(viewsets.ModelViewSet, CommentMixin):
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
            'Missing required field \'podcast\''
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


class EpisodeReceiptViewSet(viewsets.ModelViewSet):
    queryset = EpisodeReceipt.objects.all()
    serializer_class = EpisodeReceiptSerializer
    filter_class = EpisodeReceiptFilter
    lookup_field = 'episode'

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
        assert 'episode' in request.data, (
            'Missing required field \'episode\''
        )

        try:
            if 'user' in request.data:
                user = User.objects.get(id=request.data['user'])
            else:
                user = self.request.user
            episode = Episode.objects.get(id=request.data['episode'])
            instance, created = EpisodeReceipt.objects.get_or_create(episode=episode, user=user)
            if instance.completed:
                request.data['completed'] = True
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
