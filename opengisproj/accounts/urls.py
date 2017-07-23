""" accounts URL Configuration """

from django.conf.urls import url
from django.contrib.auth.views import login
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'', RedirectView.as_view(url="/account/login/", permanent=False)),
]
