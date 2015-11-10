# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool

from lab_members.models import Scientist

class LabMembersMenu(CMSAttachMenu):
    name = _("Lab Members Menu")

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        nodes = []
        for scientist in Scientist.objects.filter(current=True, visible=True):
            node = NavigationNode(
                scientist.full_name,
                reverse('lab_members:scientist_detail', args=(scientist.slug,)),
                scientist.slug
            )
            nodes.append(node)

        if Scientist.objects.filter(current=False, visible=True):
            node = NavigationNode(
                'Lab Alumni',
                reverse('lab_members:scientist_list') + '#lab-alumni',
                scientist.slug
            )
            nodes.append(node)

        return nodes

menu_pool.register_menu(LabMembersMenu)
