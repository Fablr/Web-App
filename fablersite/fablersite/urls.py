from django.conf.urls import url, patterns, include
from django.contrib import admin
from rest_framework import routers, views, reverse, response

from authentication.views import UserViewSet, GroupViewSet, UserProfileViewSet, register_by_access_token
from feed.views import FollowingViewSet, EventViewSet, FeedViewSet
from podcast.views import PodcastViewSet, EpisodeViewSet, PublisherViewSet, SubscriptionViewSet, EpisodeReceiptViewSet
from threaded_comments.views import CommentFlagViewSet, CommentViewSet, VoteViewSet

admin.autodiscover()

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
                    ret[key] = reverse.reverse(url_name, request=request, format=format)
                for api_view_key in api_view_urls.keys():
                    ret[api_view_key] = reverse.reverse(api_view_urls[api_view_key].name, request=request, format=format)
                return response.Response(ret)

        return APIRoot.as_view()

router = HybridRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
router.register('userprofile', UserProfileViewSet)
router.register('podcast', PodcastViewSet)
router.register('episode', EpisodeViewSet)
router.register('publisher', PublisherViewSet)
router.register('commentflag', CommentFlagViewSet)
router.register('subscription', SubscriptionViewSet)
router.register('comment', CommentViewSet)
router.register('vote', VoteViewSet)
router.register('episodereceipt', EpisodeReceiptViewSet)
router.register('following', FollowingViewSet)
router.register('event', EventViewSet, 'event')
router.register('feed', FeedViewSet, 'feed')

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^(?P<backend>[^/]+)/$', register_by_access_token),
)
