from django.contrib import admin

from antragsfabrik.models import Application, Type, LQFBInitiative


class LQFBInitiativeInline(admin.TabularInline):
    model = LQFBInitiative
    extra = 1


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'number', 'status', 'typ', 'created']
    list_filter = ['status']
    inlines = [LQFBInitiativeInline]


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Type)