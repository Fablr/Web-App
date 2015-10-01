from django.conf.urls import url, patterns, include
from django.contrib import admin
admin.autodiscover()

from rest_framework import permissions, routers, serializers, viewsets, views, reverse, response
from rest_framework.urlpatterns import format_suffix_patterns

from authentication.views import *
from podcast.views import *
from podcast import views

#using a custom router to support both API views and viewsets
class HybridRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self._api_view_urls = {}
    def add_api_view(self, name, url):
        self._api_view_urls[name] = url
    def remove_api_view(self, name):
        del self._api_view_urls[name]
    @property
    def api_view_urls(self):
        ret = {}
        ret.update(self._api_view_urls)
        return ret

    def get_urls(self):
        urls = super(HybridRouter, self).get_urls()
        for api_view_key in self._api_view_urls.keys():
            urls.append(self._api_view_urls[api_view_key])
        return urls

    def get_api_root_view(self):
        # Copy the following block from Default Router
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        api_view_urls = self._api_view_urls

        class APIRoot(views.APIView):
            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse(url_name, request=request, format=format)
                # In addition to what had been added, now add the APIView urls
                for api_view_key in api_view_urls.keys():
                    ret[api_view_key] = reverse(api_view_urls[api_view_key].name, request=request, format=format)
                return response.Response(ret)

        return APIRoot.as_view()

# Routers provide an easy way of automatically determining the URL conf
router = HybridRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'userprofile', UserProfileViewSet)
router.register(r'podcast', PodcastViewSet)
router.register(r'episode', EpisodeViewSet)
router.register(r'publisher', PublisherViewSet)
router.add_api_view("episodethread",  url('^episodethread/$', views.EpisodeThreadList.as_view(), name='episode-thread'))
router.add_api_view("episodecomment",  url('^episodecomment/$', views.EpisodeCommentsDetail.as_view(), name='episode-detail'))
#router.register(r'comment', CommentViewSet)
#router.register(r'threadedcomments', ThreadedCommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('^episodethread/(?P<pk>[0-9]+)/$', views.EpisodeThreadList.as_view()),
    url('^episodecomments/(?P<pk>[0-9]+)/$', views.EpisodeCommentsDetail.as_view(), name='episode-comments'),
    url('^vote/$', views.VoteDetail.as_view(), name='vote'),
    url(r'^(?P<backend>[^/]+)/$', register_by_access_token),
)

