from django.conf.urls import url, patterns, include
from django.contrib import admin
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets

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
router.register(r'comment', CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<backend>[^/]+)/$',
        register_by_access_token),
    url('', include('social.apps.django_app.urls', namespace='social')),
)
