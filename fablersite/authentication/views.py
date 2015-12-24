from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.context import RequestContext
from django import forms
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, permissions, mixins

from authentication.models import UserProfile
from authentication.forms import UserCreateForm
from authentication.serializers import *
from authentication.permissions import IsStaffOrTargetUser

from feed.models import Following

from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth import login
from social.apps.django_app.utils import psa
from .utils import get_access_token

import django_filters

def home(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
   return render_to_response('registration/home.html',
                             context_instance=context)

class RegistrationView(CreateView):
    '''
    Outputs RegistrationForm onto registration.html
    '''
    template_name = 'registration/registration.html'
    form_class = UserCreateForm
    success_url = '/status/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        return super(RegistrationView, self).form_valid(form)

# When we send a third party access token to that view
# as a GET request with access_token parameter,
# python social auth communicate with
# the third party and request the user info to register or
# sign in the user. Magic. Yeah.
@psa('social:complete')
def register_by_access_token(request, backend):
    token = request.GET.get('access_token')
    # here comes the magic
    user = request.backend.do_auth(token)
    if user:
        login(request, user)
        # that function will return our own
        # OAuth2 token as JSON
        return get_access_token(user)
    else:
        # If there was an error... you decide what you do here
        return HttpResponse("error")

'''
Deprecated View that should be removed for production.
'''
class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route()
    def current(self, serializer):
        user = self.request.user
        serializer = UserSerializer(user, many=False, context={'request': self.request})
        return Response(serializer.data)

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class UserProfileViewSet(mixins.CreateModelMixin , mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @list_route()
    def current(self, serializer):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset())
        profile = get_object_or_404(queryset, pk=user.pk)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def followers(self, request, pk):
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, pk=pk)
        followers_user = Following.objects.filter(following=profile.user).values_list('follower', flat=True)
        followers_profile = queryset.filter(user__in=followers_user)
        serializer = self.get_serializer(followers_profile, many=True, context={'request': self.request})
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def following(self, request, pk):
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, pk=pk)
        following_users = Following.objects.filter(follower=profile.user).values_list('following', flat=True)
        following_profiles = queryset.filter(user__in=following_users)
        serializer = self.get_serializer(following_profiles, many=True, context={'request': self.request})
        return Response(serializer.data)
