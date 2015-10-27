from cms.admin.pageadmin import PageAdmin as _PageAdmin
from cms.models import Page
from django.contrib import admin, messages
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, get_object_or_404
from .utils import export_page


class PageAdmin(_PageAdmin):
    def export(self, request, object_id):
        page = get_object_or_404(Page, pk=object_id)
        export_page(page, language=request.LANGUAGE_CODE)
        messages.add_message(request, messages.INFO,
                             '"%s" %s' % (str(page), _('exported')))

        return redirect(page.get_absolute_url(request.LANGUAGE_CODE))

    def get_urls(self):
        return [
            url(r'^([0-9]+)/export/$', self.export, name='cms_page_export'),
        ] + super(PageAdmin, self).get_urls()

admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)
