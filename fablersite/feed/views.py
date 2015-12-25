from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from feed.models import *
from feed.serializers import *

import django_filters

from rest_framework.decorators import api_view, list_route
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, generics, status, viewsets
from rest_framework.reverse import reverse

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

    """
    Create a model instance.
    """
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
