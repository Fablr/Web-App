from django.shortcuts import render
from django import forms
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from main.models import UserProfile
from main.forms import UserCreateForm

class RegistrationView(CreateView):
    '''
    Outputs RegistrationForm onto registration.html
    '''
    template_name = 'registration/registration.html'
    form_class = UserCreateForm
    success_url = '/registration/success/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        return super(RegistrationView, self).form_valid(form)




