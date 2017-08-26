""" accounts URL Configuration """

from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView
from .forms import LoginForm
from . import views


urlpatterns = [
    url(r'^login/?$', login, {'template_name': 'accounts/login.html', 'authentication_form': LoginForm, 'redirect_authenticated_user':True}, name="login"),
    url(r'^logout/?$', logout, {'next_page': '/portal'}, name="logout"),
    url(r'', RedirectView.as_view(url="/account/login/", permanent=False)),
]
