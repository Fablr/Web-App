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
