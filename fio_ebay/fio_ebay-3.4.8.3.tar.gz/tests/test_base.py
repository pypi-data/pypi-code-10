# -*- coding: utf-8 -*-
"""
    test_base

    :copyright: (c) 2013-2015 by Openlabs Technologies & Consulting (P) Limited
    :license: GPLv3, see LICENSE for more details.
"""
import os
import json
import unittest
from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, USER
from trytond.transaction import Transaction


ROOT_JSON_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'json'
)


def load_json(resource, filename):
    """Reads the json file from the filesystem and returns the json loaded as
    python objects

    On filesystem, the files are kept in this format:
        json----
              |
            resource----
                       |
                       filename

    :param resource: The ebay resource for which the file has to be
                     fetched. It is same as the folder name in which the files
                     are kept.
    :param filename: The name of the file to be fethced without `.json`
                     extension.
    :returns: Loaded json from the contents of the file read.
    """
    file_path = os.path.join(
        ROOT_JSON_FOLDER, resource, str(filename)
    ) + '.json'

    return json.loads(open(file_path).read())


class TestBase(unittest.TestCase):
    """
    Setup basic defaults
    """

    def setUp(self):
        """
        Set up data used in the tests.
        this method is called before each test function execution.
        """
        trytond.tests.test_tryton.install_module('ebay')

    def setup_defaults(self):
        """
        Setup default data
        """
        self.Uom = POOL.get('product.uom')
        self.Currency = POOL.get('currency.currency')
        self.Company = POOL.get('company.company')
        self.Party = POOL.get('party.party')
        self.Country = POOL.get('country.country')
        self.Subdivision = POOL.get('country.subdivision')
        self.AccountTemplate = POOL.get('account.account.template')
        self.Account = POOL.get('account.account')
        self.CreateChartAccount = POOL.get(
            'account.create_chart', type="wizard"
        )
        self.User = POOL.get('res.user')
        self.PaymentTerm = POOL.get('account.invoice.payment_term')
        self.FiscalYear = POOL.get('account.fiscalyear')
        self.Sequence = POOL.get('ir.sequence')
        self.SequenceStrict = POOL.get('ir.sequence.strict')
        self.AccountConfiguration = POOL.get('account.configuration')
        self.Property = POOL.get('ir.property')
        self.ModelField = POOL.get('ir.model.field')
        self.SaleChannel = POOL.get('sale.channel')
        self.Location = POOL.get('stock.location')
        self.PriceList = POOL.get('product.price_list')

        with Transaction().set_context(company=None):
            self.party, = self.Party.create([{
                'name': 'ABC',
            }])
            self.usd, = self.Currency.create([{
                'name': 'US Dollar',
                'code': 'USD',
                'symbol': '$',
            }])
            self.company, = self.Company.create([{
                'party': self.party.id,
                'currency': self.usd.id,
            }])

        self.User.write([self.User(USER)], {
            'main_company': self.company.id,
            'company': self.company.id,
        })

        date = datetime.utcnow().date()

        with Transaction().set_context(
            self.User.get_preferences(context_only=True)
        ):

            invoice_sequence, = self.SequenceStrict.create([{
                'name': '%s' % date.year,
                'code': 'account.invoice',
                'company': self.company.id,
            }])
            fiscal_year, = self.FiscalYear.create([{
                'name': '%s' % date.year,
                'start_date': date + relativedelta(month=1, day=1),
                'end_date': date + relativedelta(month=12, day=31),
                'company': self.company.id,
                'post_move_sequence': self.Sequence.create([{
                    'name': '%s' % date.year,
                    'code': 'account.move',
                    'company': self.company.id,
                }])[0].id,
                'out_invoice_sequence': invoice_sequence.id,
                'in_invoice_sequence': invoice_sequence.id,
                'out_credit_note_sequence': invoice_sequence.id,
                'in_credit_note_sequence': invoice_sequence.id,
            }])
            self.FiscalYear.create_period([fiscal_year])

            account_template, = self.AccountTemplate.search(
                [('parent', '=', None)]
            )
            session_id, _, _ = self.CreateChartAccount.create()
            create_chart = self.CreateChartAccount(session_id)
            create_chart.account.account_template = account_template
            create_chart.account.company = self.company.id
            create_chart.transition_create_account()

            revenue, = self.Account.search([
                ('kind', '=', 'revenue'),
                ('company', '=', self.company.id),
            ])
            receivable, = self.Account.search([
                ('kind', '=', 'receivable'),
                ('company', '=', self.company.id),
            ])
            payable, = self.Account.search([
                ('kind', '=', 'payable'),
                ('company', '=', self.company.id),
            ])
            expense, = self.Account.search([
                ('kind', '=', 'expense'),
                ('company', '=', self.company.id),
            ])

            create_chart.properties.company = self.company
            create_chart.properties.account_receivable = receivable
            create_chart.properties.account_payable = payable
            create_chart.properties.account_revenue = revenue
            create_chart.properties.account_expense = expense
            create_chart.transition_create_properties()

        self.AccountConfiguration.write(
            [self.AccountConfiguration(1)], {
                'default_account_receivable': receivable.id,
                'default_account_payable': payable.id
            })

        self.Party.write(
            [self.party], {
                'account_payable': payable.id,
                'account_receivable': receivable.id,
            }
        )

        # Create payment term
        self.payment_term, = self.PaymentTerm.create([{
            'name': 'Direct',
            'lines': [('create', [{'type': 'remainder'}])]
        }])

        self.country_us, = self.Country.create([{
            'name': 'United States',
            'code': 'US',
        }])

        self.country_in, = self.Country.create([{
            'name': 'India',
            'code': 'IN',
        }])

        self.subdivision_fl, = self.Subdivision.create([{
            'name': 'Florida',
            'code': 'US-FL',
            'country': self.country_us.id,
            'type': 'state',
        }])

        self.subdivision_wa, = self.Subdivision.create([{
            'name': 'Washington',
            'code': 'US-WA',
            'country': self.country_us.id,
            'type': 'state',
        }])

        self.subdivision_up, = self.Subdivision.create([{
            'name': 'Uttar Pradesh',
            'code': 'IN-UP',
            'country': self.country_in.id,
            'type': 'state',
        }])

        self.Subdivision.create([{
            'name': 'New Delhi',
            'code': 'IN-DL',
            'type': 'state',
            'country': self.country_in.id,
        }])

        model_field, = self.ModelField.search([
            ('name', '=', 'account_revenue'),
            ('model.model', '=', 'product.template'),
        ], order=[], limit=1)

        self.uom, = self.Uom.search([
            ('name', '=', 'Unit'),
        ])
        warehouse, = self.Location.search([
            ('type', '=', 'warehouse')
        ], limit=1)

        self.price_list = self._create_pricelist()

        self.ebay_channel, = self.SaleChannel.create([{
            'name': 'eBay Account',
            'warehouse': warehouse.id,
            'company': self.company.id,
            'source': 'ebay',
            'currency': self.company.currency.id,
            'price_list': self.price_list,
            'invoice_method': 'manual',
            'shipment_method': 'manual',
            'payment_term': self.payment_term,
            'ebay_app_id': 'test_app_id_by_ebay',
            'ebay_dev_id': 'test_dev_id_by_ebay',
            'ebay_cert_id': 'test_cert_id_by_ebay',
            'ebay_token': 'a long test token by ebay',
            'is_ebay_sandbox': True,
            'default_uom': self.uom.id,
        }])

        # TODO: This should work without creating new properties
        self.Property.create([{
            'value': '%s,%s' % (
                'account.account', self.get_account_by_kind('revenue')
            ),
            'res': None,
            'field': model_field.id,
        }])

    def _create_pricelist(self):
        """
        Create the pricelists
        """
        return self.PriceList.create([{
            'name': 'PL 1',
            'company': self.company.id,
            'lines': [
                ('create', [{
                    'formula': 'unit_price * %s' % Decimal('1.10')
                }])
            ],
        }])[0]

    def get_account_by_kind(self, kind, company=None, silent=True):
        """Returns an account with given spec

        :param kind: receivable/payable/expense/revenue
        :param silent: dont raise error if account is not found
        """
        Account = POOL.get('account.account')
        Company = POOL.get('company.company')

        if company is None:
            company, = Company.search([], limit=1)

        accounts = Account.search([
            ('kind', '=', kind),
            ('company', '=', company.id)
        ], limit=1)
        if not accounts and not silent:
            raise Exception("Account not found")
        return accounts and accounts[0].id or None
