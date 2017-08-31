from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^home/?$', views.home, name='home'),
    url(r'^add/?$', views.add, name='add-data'),
    url(r'^browse/?$', views.browse, name='browse-data'),
    url(r'^parameters/?$', views.addParam, name='parameters'),
    url(r'^datagroups/?$', views.dataGroups, name='datagroups'),
    url(r'^reports/?$', views.reports, name='reports'),
    url(r'^shapefiles/?$', views.shapefilesManager, name='shapefiles'),
    url(r'^importer/?$', views.importView, name='importer'),
    url(r'^ajax/(?P<action>[a-zA-Z]*)/?$', views.processAjax, name='ajax'),
    url(r'^fileupload/?$', views.fileupload, name='upload-manager'),
    url(r'^/?$', RedirectView.as_view(url='/portal/home')),
    url(r'', views.pageNotFound, name='404')
]