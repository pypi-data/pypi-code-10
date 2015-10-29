from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import CorrectivProvider

urlpatterns = default_urlpatterns(CorrectivProvider)
