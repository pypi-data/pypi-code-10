# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break, SubMenu
from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK

@toolbar_pool.register
class LabMembersToolbar(CMSToolbar):

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(
            ADMIN_MENU_IDENTIFIER, _('Apps')
        )

        position = admin_menu.get_alphabetical_insert_position(
            _('Lab Members'),
            SubMenu
        )

        if not position:
            position = admin_menu.find_first(
                Break,
                identifier=ADMINISTRATION_BREAK
            ) + 1
            admin_menu.add_break('custom-break', position=position)

        lab_members_menu = admin_menu.get_or_create_menu(
            'lab-members-menu',
            _('Lab Members ...'),
            position=position
        )

        url_change = reverse('admin:lab_members_scientist_changelist')
        url_addnew = reverse('admin:lab_members_scientist_add')
        lab_members_menu.add_sideframe_item(_('Edit Scientists'), url=url_change)
        lab_members_menu.add_modal_item(_('Add New Scientist'), url=url_addnew)
        lab_members_menu.add_break()

        url_change = reverse('admin:lab_members_position_changelist')
        url_addnew = reverse('admin:lab_members_position_add')
        lab_members_menu.add_sideframe_item(_('Edit Positions'), url=url_change)
        lab_members_menu.add_modal_item(_('Add New Position'), url=url_addnew)
        lab_members_menu.add_break()

        url_change = reverse('admin:lab_members_institution_changelist')
        url_addnew = reverse('admin:lab_members_institution_add')
        lab_members_menu.add_sideframe_item(_('Edit Institutions'), url=url_change)
        lab_members_menu.add_modal_item(_('Add New Institution'), url=url_addnew)
        lab_members_menu.add_break()

        url_change = reverse('admin:lab_members_field_changelist')
        url_addnew = reverse('admin:lab_members_field_add')
        lab_members_menu.add_sideframe_item(_('Edit Fields of Study'), url=url_change)
        lab_members_menu.add_modal_item(_('Add New Field of Study'), url=url_addnew)
        lab_members_menu.add_break()

        url_change = reverse('admin:lab_members_degree_changelist')
        url_addnew = reverse('admin:lab_members_degree_add')
        lab_members_menu.add_sideframe_item(_('Edit Degrees'), url=url_change)
        lab_members_menu.add_modal_item(_('Add New Degree'), url=url_addnew)
        lab_members_menu.add_break()

        url_change = reverse('admin:lab_members_advisor_changelist')
        url_addnew = reverse('admin:lab_members_advisor_add')
        lab_members_menu.add_sideframe_item(_('Edit Advisors'), url=url_change)
        lab_members_menu.add_modal_item(_('Add New Advisor'), url=url_addnew)

