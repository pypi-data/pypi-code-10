from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^([a-z_]+)/([0-9]+)/([a-z_]+)/?$', 'mint.views.with_id'),
    url(r'^([a-z_]+)/([0-9]+)/?$', 'mint.views.with_id'),
    url(r'^([a-z_]+)/([a-z_]+)/?$', 'mint.views.without_id'),
    url(r'^([a-z_]+)/?$', 'mint.views.without_id'),
)