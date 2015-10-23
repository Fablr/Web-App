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
from django.contrib import admin
admin.autodiscover()

from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^.*$', TemplateView.as_view(template_name="index.html")),
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^', include('podcast.urls', namespace="podcast")),

    #in-house apps
    #url(r'^registration/', include('authentication.urls', namespace="registration")),
    #url(r'^$', TemplateView.as_view(template_name='status.html')),
    
    #url('^accounts/', include('django.contrib.auth.urls', namespace="accounts")),
    #url('', include('social.apps.django_app.urls', namespace='social')),
    #url('', include('django.contrib.auth.urls', namespace='auth')),
    #url(r'^login/', include('login.urls', namespace="login")),
    #url(r'', include(splash.urls)),
)

#if settings.DEBUG:
#    urlpatterns += patterns('django.contrib.staticfiles.views',
#        url(r'', 'serve', {
#            'document_root': settings.STATIC_ROOT, 
#            'path': '/base.html'}
#        ),
#    )
