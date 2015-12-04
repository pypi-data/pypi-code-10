from django.conf import settings
from django.core import urlresolvers

from .utils import refresh_permissions, generate_permissions


def autodiscover():
    """Autodiscover for urls.py"""
    # Get permissions based on urlpatterns from urls.py
    url_conf = getattr(settings, 'ROOT_URLCONF', ())
    resolver = urlresolvers.get_resolver(url_conf)
    urlpatterns = resolver.url_patterns
    permissions = generate_permissions(urlpatterns)
    # Refresh permissions
    refresh_permissions(permissions)
