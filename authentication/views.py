from django.shortcuts import render
from django import forms
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, permissions

from authentication.models import UserProfile
from authentication.forms import UserCreateForm
from authentication.serializers import *
from authentication.permissions import IsStaffOrTargetUser

import django_filters

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
