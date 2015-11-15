# -*- coding:utf-8 -*-
'''
Created on Nov 14, 2015

@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

from ics2caldav import Ical2CalDav
from patches import patch_module_caldav, patch_module_ics


# fix needed for redmine Redmics plugin

patch_module_caldav()
patch_module_ics()


class Redmine2Owncloud(Ical2CalDav):
    # fix needed for redmine Redmics plugin
    def fix_uid(self, uid):
        # the `:` is not valid in path on windows system
        uid = uid.replace(':', '_')
        i = uid.find('issue_')
        if i == -1:
            i = uid.find('version_')

        if i > 0:
            uid = uid[i:]

        return uid
