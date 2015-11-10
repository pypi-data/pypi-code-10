from django.conf.urls import patterns, url
from lab_members.views import ScientistListView, ScientistDetailView

urlpatterns = patterns('',
    url(r'^$', ScientistListView.as_view(), name='scientist_list'),
    url(r'^(?P<slug>[^/]+)/$', ScientistDetailView.as_view(), name='scientist_detail'),
)
