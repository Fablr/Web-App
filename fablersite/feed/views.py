from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404
import django_filters
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

from authentication.models import User
from feed.models import Following, Event
from feed.serializers import FollowingSerializer, EventSerializer, FeedSerializer

class FollowingFilter(django_filters.FilterSet):
    class Meta:
        model = Following
        fields = ['following', 'follower']

class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    filter_class = FollowingFilter
    lookup_field = 'following'

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

        follower = self.request.user

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg], 'follower': follower}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        assert 'following' in request.data, (
            'Missing required field `following`'
        )

        try:
            follower = self.request.user
            following = User.objects.get(pk=request.data['following'])
            instance, created = Following.objects.get_or_create(follower=follower, following=following)
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

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class FeedViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = FeedSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        assert self.lookup_field in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, self.lookup_field)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        user = get_object_or_404(User.objects.all(), **filter_kwargs)

        following = Following.objects.filter(follower=user).values_list('following', flat=True)
        queryset = queryset.filter(user__in=following)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
