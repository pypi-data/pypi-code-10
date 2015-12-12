from django.conf.urls import patterns, url
from .views import EmailAlternativeView


urlpatterns = patterns(
    '',
    url(r'^email_alternative/(?P<pk>\d+)/$',
        EmailAlternativeView.as_view(),
        name='email_alternative'),
)