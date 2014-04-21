from django.conf.urls import patterns, url

from antragsfabrik import views

urlpatterns = patterns('', url(r'^$', views.index, name='index'),
                       url(r'^profile/$', views.profile_edit, name='profile_edit'),
                       url(r'^create/$', views.appl_create, name='appl_create'),
                       url(r'^typ/(?P<typ_id>\d+)/$', views.typ_index, name='typ_index'),
                       url(r'^typ/(?P<typ_id>\d+)/(?P<page>\d+)/$', views.typ_index, name='typ_index_page'),
                       url(r'^appl/(?P<application_id>\d+)/$', views.appl_detail, name='appl_detail'),
                       url(r'^appl/(?P<application_id>\d+)/edit/$', views.appl_edit, name='appl_edit'),
                       url(r'^appl/(?P<application_id>\d+)/submit/$', views.appl_submit, name='appl_submit'),
                       url(r'^appl/(?P<application_id>\d+)/cancel/$', views.appl_cancel, name='appl_cancel'),
                       url(r'^appl/(?P<application_id>\d+)/setnumber/$', views.appl_set_number, name='appl_set_number'),)