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
import django.conf.urls
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
urlpatterns = django.conf.urls.patterns('',
    django.conf.urls.url(r'^', django.conf.urls.include(router.urls)),
    django.conf.urls.url(r'^api-auth/', django.conf.urls.include('rest_framework.urls', namespace='rest_framework')),
    django.conf.urls.url(r'^o/', django.conf.urls.include('oauth2_provider.urls', namespace='oauth2_provider')),
    django.conf.urls.url(r'^admin/', django.conf.urls.include(admin.site.urls)),
    django.conf.urls.url(r'^', django.conf.urls.include('podcast.urls', namespace="podcasts")),
    #(r'^', include('registration.backends.default.urls')),

    #in-house apps
    django.conf.urls.url(r'^registration/', django.conf.urls.include('authentication.urls', namespace="registration")),
    django.conf.urls.url(r'^status/', TemplateView.as_view(template_name='status.html')),
    
    django.conf.urls.url('^', django.conf.urls.include('django.contrib.auth.urls', namespace="accounts")),
    #url(r'^login/', include('login.urls', namespace="login")),
    #url(r'', include(splash.urls)),
)
