# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from antragsfabrik.apiviews import ApplicationViewSet, TypeViewSet, UserViewSet

router = DefaultRouter()
router.register(r'appl', ApplicationViewSet)
router.register(r'typ', TypeViewSet)
router.register(r'user', UserViewSet)

urlpatterns = patterns('', url(r'^', include(router.urls)))