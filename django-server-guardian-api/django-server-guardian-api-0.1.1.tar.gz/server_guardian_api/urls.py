"""URLs for the server_guardian_api app."""
from compat import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$',
        views.ServerGuardianAPIView.as_view(),
        name='server_guardian_api'),
)
