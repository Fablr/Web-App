from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^publisher_(?P<pk>[\w\-]+)/$', views.PublisherDetailView.as_view(), name='publisher_detail'),
    url(r'^podcast_(?P<pk>[\w\-]+)/$', views.PodcastDetailView.as_view(), name='podcast_detail'),
    url(r'^episode_(?P<pk>[\w\-]+)/$', views.EpisodeDetailView.as_view(), name='episode_detail'),
#    url(r'^publisher_(?P<publisherid>[\w\-]+)/podcast_(?P<podcastid>[\w\-]+)/episode_(?P<episodeid>\d+)/$', views.EpisodeDetailView.as_view(), name='episode_detail'),
    #url(r'^success$', login_required(views.StatusView.as_view()), name='status'),
]
