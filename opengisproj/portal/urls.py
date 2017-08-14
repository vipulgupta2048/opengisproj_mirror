from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^home/?$', views.home),
    url(r'^add/?$', views.add),
    url(r'^browse/?$', views.browse),
    url(r'^parameters/?$', views.addParam),
    url(r'^reports/?$', views.reports),
    url(r'^importView/?$', views.importView),
#    url(r'^import/?$', views.model_form_upload),
    url(r'^ajax/(?P<action>[a-zA-Z]*)/?$', views.processAjax),
    url(r'^install/?$', views.demo),
    url(r'', RedirectView.as_view(url="/portal/home/", permanent=True))
]