# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import template
from antragsfabrik.models import Application

register = template.Library()


def key(d, key_name):
    try:
        value = d[key_name]
    except KeyError:
        from django.conf import settings

        value = settings.TEMPLATE_STRING_IF_INVALID

    return value


key = register.filter('key', key)


def status_name(status):
    for st in Application.STATUS_CHOICES:
        if st[0] == status:
            return st[1]
    return status


key = register.filter('status_name', status_name)