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