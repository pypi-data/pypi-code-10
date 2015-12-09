# -*- coding: utf-8 -*-

from . import register


@register
def nowtime():
    from datetime import datetime
    return datetime.now()
