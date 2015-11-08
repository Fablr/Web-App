from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django import forms
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, permissions

from authentication.models import UserProfile
from authentication.forms import UserCreateForm
from authentication.serializers import *
from authentication.permissions import IsStaffOrTargetUser

from rest_framework.decorators import list_route
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



class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User

# Django Rest API
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (permissions.AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),

    @list_route()
    def current(self, serializer):
        user = self.request.user
        serializer = UserSerializer(user, many=False, context={'request': self.request})
        return Response(serializer.data)

class GroupViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    permission_classes = [permissions.IsAuthenticated]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer



#from permissions import IsAuthenticatedOrCreate
#from rest_framework.authentication import BasicAuthentication
#
#class SignUp(generics.CreateAPIView):
#    '''
#    Signup view for API with oauth
#    '''
#    queryset = User.objects.all()
#    serializer_class = SignUpSerializer
#    permission_classes = (IsAuthenticatedOrCreate,)

#class Login(generics.ListAPIView):
#    '''
#    Login view for API with oauth
#    '''
#    queryset = User.objects.all()
#    serializer_class = LoginSerializer

    #BasicAuthentication needs to change to SessionAuthentication or some other variant
#    authentication_classes = (BasicAuthentication,)

#    def get_queryset(self):
#        return [self.request.user]
