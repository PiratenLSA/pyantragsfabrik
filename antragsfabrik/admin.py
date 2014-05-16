# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from antragsfabrik.models import Application, Type, LQFBInitiative


class LQFBInitiativeInline(admin.TabularInline):
    model = LQFBInitiative
    extra = 1


class ApplicationAdmin(SimpleHistoryAdmin):
    list_display = ['title', 'number', 'status', 'typ', 'created']
    list_filter = ['status']
    inlines = [LQFBInitiativeInline]


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Type)