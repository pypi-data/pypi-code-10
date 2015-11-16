from django.conf.urls import patterns, url

from .views import DocumentFileView

urlpatterns = patterns('',
  url(r'^(?P<slug>[\w-]+)/(?P<object_id>[0-9]+$)', DocumentFileView.as_view(), name='print'),
)