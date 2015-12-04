from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^item/(?P<pk>\d+)/$', RedirectView.as_view(url='/admin/'), name='mojo_navigation_tests_item')
]
