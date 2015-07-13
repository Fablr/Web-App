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
from django.views.generic import TemplateView
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from authentication.views import *
from podcast.views import *



# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'userprofile', UserProfileViewSet)
router.register(r'podcast', PodcastViewSet)
router.register(r'episode', EpisodeViewSet)
router.register(r'publisher', PublisherViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
    #(r'^', include('registration.backends.default.urls')),

    #in-house apps
    url(r'^registration/', include('authentication.urls', namespace="registration")),
    url(r'^status/', TemplateView.as_view(template_name='status.html')),
    
    url('^', include('django.contrib.auth.urls', namespace="accounts")), 
    #url(r'^login/', include('login.urls', namespace="login")),
    #url(r'', include(splash.urls)),
)
