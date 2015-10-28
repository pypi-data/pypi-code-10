# -*- coding: utf-8 -*-
"""
URLs for the subscriber module.
"""
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^thank-you/$', TemplateView.as_view(template_name="subscriber/thank_you.html"), name="thank_you"),
    url(
        r'^successful-unsubscribe/$',
        TemplateView.as_view(template_name="subscriber/successful_unsubscribe.html"),
        name="successful_unsubscribe"
    ),
)

urlpatterns += patterns(
    'holding_page.subscribers.admin_views',
    url(r'^admin/data/export/$', 'export_csv', name="export_csv"),
)

urlpatterns += patterns(
    'holding_page.subscribers.views',
    url(r'^unsubscribe/(?P<email>.+)/$', 'unsubscribe_form', name="unsubscribe_form_with_email"),
    url(r'^unsubscribe/$', 'unsubscribe_form', name="unsubscribe_form"),
    url(
        r'^(?P<code>[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-[0-9A-Za-z]{4}-[0-9A-Za-z]{4}-[0-9A-Za-z]{12})/$',
        'subscriber_form',
        name="subscriber_form_with_code"
    ),
    url(r'^$', 'subscriber_form', name="subscriber_form"),
)
