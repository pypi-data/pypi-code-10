# -*- coding: utf-8 -*-
from __future__ import absolute_import


def get_client_ip(request):
    """Get the IP address of the client, taking into account the X-Forwarded-For header"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')
