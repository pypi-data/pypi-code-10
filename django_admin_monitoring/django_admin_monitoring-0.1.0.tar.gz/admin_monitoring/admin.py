from django import forms
from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.template import Template, Context


def admin_monitoring_mixin_factory(**filter_kwargs):

    class AdminMonitoringMixin(admin.ModelAdmin):
        def get_css_name(self):
            return '%s_%s_info_css' % (self.model._meta.app_label, self.model._meta.model_name)

        def get_urls(self):
            urls = super(AdminMonitoringMixin, self).get_urls()
            additional_urls = patterns('',
                url(r'^info.css$', self.admin_site.admin_view(self.get_css_view), name=self.get_css_name())
            )
            return additional_urls + urls

        def get_css_view(self, request):
            new_items = self.model.objects.filter(**filter_kwargs)
            template = Template("""
                {% load admin_monitoring_tags %}
                {% if items %}{% for item in items %}a[href="{% get_admin_change_url item %}"]{% if not forloop.last %},{% endif %} {% endfor %}{
                    font-weight: bold;
                    text-decoration: underline;
                    color: red;
                }{% endif %}
            """)

            return HttpResponse(template.render(Context({
                'items': new_items
            })), content_type="text/css")

        def _media(self):
            return forms.Media(css={
                'screen': (reverse_lazy('admin:%s' % self.get_css_name()), )
            })
        media = property(_media)

    return AdminMonitoringMixin
