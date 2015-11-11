from django.contrib import admin
from blacklist import models
from django.utils.translation import ugettext_lazy as _


class BlockRulesAdmin(admin.ModelAdmin):
    fieldsets = (
        (_("Rule type"), {
            'fields': ('enabled', 'reason'),
            'description': _('Fields below describes the rule'),
        }),
        (_("Client options"), {
            'fields': ('ip', 'subnet', 'country', 'user_agent'),
            'description': _('Fields below identifies client'),
        }),
        (_('Page options'), {
            'fields': ('method', 'path', 'view'),
            'description': _('Fields below identifies site-specific information')
        }),
    )
    list_display = ('reason', 'enabled', 'ip', 'subnet', 'country', 'user_agent', 'view', 'path', 'method', 'created', 'updated')
    list_display_links = list_display
    list_filter = ('method', 'view')
    search_fields = ('ip', 'subnet', 'user_agent', 'path')


admin.site.register(models.BlockRules, BlockRulesAdmin)


class RequestLogAdmin(admin.ModelAdmin):
    fieldsets = (
        (_("Client options"), {
            'fields': ('ip', 'user_agent'),
            'description': _('Fields below identifies client'),
        }),
        (_('Page options'), {
            'fields': ('method', 'path', 'view'),
            'description': _('Fields below identifies site-specific information')
        }),
    )
    list_display = ('ip', 'country', 'user_agent', 'view', 'path', 'method', 'created')
    list_filter = ('method', 'view')
    search_fields = ('ip', 'user_agent', 'path')

admin.site.register(models.RequestLog, RequestLogAdmin)

admin.site.register(models.Country)
