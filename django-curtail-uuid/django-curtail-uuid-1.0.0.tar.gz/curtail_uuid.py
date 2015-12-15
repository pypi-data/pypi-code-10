# -*- coding: utf-8 -*-

from django.conf import settings

import shortuuid


class _CurtailUUID:
    def __init__(self):
        self.length = hasattr(settings, 'CURTAIL_UUID_LENGTH') and settings.CURTAIL_UUID_LENGTH or 22

    def uuid(self, model, field='uuid', length=None):
        flag = True
        while flag:
            uuid = shortuuid.ShortUUID().random(length=length or self.length)
            try:
                model.objects.get(**{field: uuid})
            except model.DoesNotExist:
                flag = False
        return uuid


# For backwards compatibility
CurtailUUID = _CurtailUUID()
