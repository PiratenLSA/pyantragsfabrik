from django.conf.urls import patterns, url

from antragsfabrik import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^typ/(?P<typ_id>\d+)/$', views.typ_index, name='typ_index'),
    url(r'^typ/(?P<typ_id>\d+)/(?P<page>\d+)/$', views.typ_index, name='typ_index_page'),
    url(r'^(?P<application_id>\d+)/$', views.detail, name='detail'),
)