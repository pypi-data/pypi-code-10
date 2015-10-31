from django.conf.urls import include, url
from .views import humanstxt

urlpatterns = [
    url(r'^$', humanstxt, name='humanstxt'),
]
