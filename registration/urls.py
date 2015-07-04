from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RegistrationView.as_view(), name='registration'),
]
