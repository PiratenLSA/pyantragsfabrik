from django.conf.urls import patterns, url

from antragsfabrik import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<application_id>\d+)/$', views.detail, name='detail'),
)