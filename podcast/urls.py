from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RegistrationView.as_view(), name='registration'),
    #url(r'^success$', login_required(views.StatusView.as_view()), name='status'),
]
