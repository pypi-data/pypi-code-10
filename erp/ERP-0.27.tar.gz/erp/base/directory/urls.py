__author__ = 'cltanuki'
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from . import api

router = DefaultRouter()
router.register(r'person', api.PersonViewSet)
# router.register(r'person/(?P<person_pk>.+)/phones', api.PhonesViewSet)
# router.register(r'person/(?P<person_pk>.+)/emails', api.EMailsViewSet)
# router.register(r'person/(?P<person_pk>.+)/positions', api.PositionsViewSet)

urlpatterns = router.urls
urlpatterns += [
    url(r'^register/$', api.NewUser.as_view()),
]
