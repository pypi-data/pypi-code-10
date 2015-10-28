# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# This file is part of Lino Cosi.
#
# Lino Cosi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Cosi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Cosi.  If not, see
# <http://www.gnu.org/licenses/>.


"""Default settings module for a :ref:`cosi` project. This is being
inherited by the other applications below :mod:`lino_cosi.projects`.

"""

from __future__ import unicode_literals

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _

import lino_cosi


class Site(Site):
    """Base class for a :ref:`cosi` application.

    """

    verbose_name = "Lino Cosi"
    version = lino_cosi.SETUP_INFO['version']
    url = lino_cosi.SETUP_INFO['url']

    demo_fixtures = 'std few_countries euvatrates few_languages furniture \
    minimal_ledger demo demo2 demo_bookings'.split()

    # languages = 'en de fr'
    languages = 'en'

    user_profiles_module = 'lino_cosi.lib.cosi.roles'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.gfks'
        # yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino_cosi.lib.contacts'
        #~ yield 'lino.modlib.households'
        yield 'lino.modlib.products'
        yield 'lino_cosi.lib.accounts'
        yield 'lino_cosi.lib.sepa'

        yield 'lino.modlib.excerpts'

        # yield 'lino.modlib.outbox'
        # yield 'lino.modlib.uploads'
        # yield 'lino.modlib.appypod'
        yield 'lino.modlib.export_excel'

        # ledger must come before sales because its demo fixture
        # creates journals

        # yield 'lino.modlib.ledger'
        yield 'lino_cosi.lib.vat'
        yield 'lino_cosi.lib.declarations'
        yield 'lino_cosi.lib.finan'
        yield 'lino_cosi.lib.sales'  # automatically added by courses
        #~ 'lino.modlib.journals',
        #~ 'lino.modlib.projects',
        #~ yield 'lino.modlib.blogs'
        #~ yield 'lino.modlib.tickets'
        #~ 'lino.modlib.links',
        #~ 'lino.modlib.thirds',
        #~ yield 'lino.modlib.postings'
        # yield 'lino.modlib.pages'
        # yield 'lino_cosi.lib.cosi'

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        """
        super(Site, self).setup_plugins()
        self.plugins.contacts.configure(hide_region=True)
        self.plugins.ledger.configure(use_pcmn=True)
        self.plugins.countries.configure(country_code='BE')

    def setup_actions(self):
        super(Site, self).setup_actions()
        partners = self.modules.contacts
        from lino.core.merge import MergeAction
        for m in (partners.Person, partners.Organisation):
            m.define_action(merge_row=MergeAction(m))

    def setup_layouts(self):
        super(Site, self).setup_layouts()

        self.modules.system.SiteConfigs.set_detail_layout("""
        site_company next_partner_id:10
        default_build_method
        clients_account   sales_account     sales_vat_account
        suppliers_account purchases_account purchases_vat_account
        """)

        self.modules.accounts.Accounts.set_detail_layout("""
        ref:10 name id:5
        seqno chart group type clearable
        ledger.MovementsByAccount
        """)


class DocsSite(Site):
    """A special variant used to build the docs.
    """
    def get_installed_apps(self):
        yield super(DocsSite, self).get_installed_apps()
        yield 'lino_cosi.lib.courses'  # needed for Sphinx autosummar
        yield 'lino_cosi.lib.vatless'

    def get_apps_modifiers(self, **kw):
        kw = super(DocsSite, self).get_apps_modifiers(**kw)
        kw.update(sales='lino_cosi.lib.auto.sales')
        return kw
