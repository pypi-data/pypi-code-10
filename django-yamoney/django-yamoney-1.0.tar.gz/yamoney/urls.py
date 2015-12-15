# -*- coding: utf-8 -*-
from django.conf.urls import *
from yamoney.views import NotificationView

urlpatterns = patterns(
    '',
    url(r'^notification/$', NotificationView.as_view(), name='yamoney_notification')
)