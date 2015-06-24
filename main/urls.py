"""fablersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, patterns, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
from . import views
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope


# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^sign_up/$', views.SignUp.as_view(), name="sign_up"),
    url(r'^login/$', views.Login.as_view(), name="login"),
)
