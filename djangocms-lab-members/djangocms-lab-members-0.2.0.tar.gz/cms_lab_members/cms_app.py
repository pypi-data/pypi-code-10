# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from cms_lab_members.menu import LabMembersMenu

class LabMembersApp(CMSApp):
    name = _("Lab Member App")
    urls = ["lab_members.urls"]
    app_name = "lab_members"
    menus = [LabMembersMenu]

apphook_pool.register(LabMembersApp)
