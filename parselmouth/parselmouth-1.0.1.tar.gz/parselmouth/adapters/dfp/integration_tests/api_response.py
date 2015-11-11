#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Acceptance checks to determine if API responses are compatible with the
current interface implementation
"""

# Future-proof
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Standard Library Imports
from datetime import datetime
from pytz import timezone
import unittest

# Rosetta Stone Imports
from parselmouth import Parselmouth
from parselmouth import ParselmouthException
from parselmouth import ParselmouthProviders
from parselmouth.delivery import Campaign
from parselmouth.delivery import Cost
from parselmouth.delivery import Creative
from parselmouth.delivery import DeliveryMeta
from parselmouth.delivery import Goal
from parselmouth.delivery import LineItem
from parselmouth.delivery import Stats
from parselmouth.targeting import TargetingData

from parselmouth.adapters.dfp.integration_tests.harness import BLOCKBUSTER_728_CREATIVE
from parselmouth.adapters.dfp.integration_tests.harness import CAMPAIGN_ID as LINE_ITEM_CAMPAIGN_ID
from parselmouth.adapters.dfp.integration_tests.harness import EXPECTED_LINE_ITEMS
from parselmouth.adapters.dfp.targeting_utils import transform_custom_targeting_from_dfp
from parselmouth.adapters.dfp.targeting_utils import transform_inventory_targeting_from_dfp


class TestApiResponse(unittest.TestCase):

    DOMAIN = 'ads.demo.com'
    CAMPAIGN_ID = '287597403'
    LINE_ITEM_ID = '150163803'
    BAD_LINE_ITEM_ID = '0'
    BAD_CREATIVE_ID = '0'
    BAD_CAMPAIGN_ID = '0'
    TEST_ADVERTISER_ID = '57947163'
    TEST_CAMPAIGN_LINE_ITEMS = LINE_ITEM_CAMPAIGN_ID

    def setUp(self):
        self.parselmouth = Parselmouth(
            provider_name=ParselmouthProviders.google_dfp_premium,
            config_path='dfp_integration_config.yaml',
        )

    def test_get_network_timezone(self):
        test_network_timezone = self.parselmouth.get_network_timezone()
        self.assertEqual(test_network_timezone, timezone('America/New_York'))

    def test_bad_campaign(self):
        with self.assertRaises(ParselmouthException):
            _ = self.parselmouth.provider.get_campaign(self.BAD_CAMPAIGN_ID)

    def test_campaign(self):

        test_campaign = self.parselmouth.get_campaign(self.CAMPAIGN_ID)

        answer_campaign = Campaign(
            advertiser_id='45402483',
            agency_id=None,
            creator_id='91002483',
            currency_code='USD',
            end=datetime(
                2015, 8, 14, 23, 59, tzinfo=timezone('America/New_York')
            ),
            external_campaign_id='0',
            id='287597403',
            name='Justins test campaign 1',
            start=datetime(
                2015, 3, 3, 15, 57, tzinfo=timezone('America/New_York')
            ),
            status='DRAFT',
            stats=Stats(
                impressions=0,
                clicks=0,
            ),
            total_budget=Cost(
                budget_micro_amount=1000000000.0,
                budget_currency_code='USD',
            ),
        )

        self.assertEqual(test_campaign, answer_campaign)

    def test_get_campaigns(self):
        expected_campaigns = set([
            Campaign(
                advertiser_id=self.TEST_ADVERTISER_ID,
                agency_id=None,
                creator_id='91002483',
                currency_code='USD',
                end=datetime(
                    2016, 3, 19, 23, 59, tzinfo=timezone('America/New_York')
                ),
                external_campaign_id='0',
                id='249699843',
                name='Blockbuster Sample Campaign',
                start=datetime(
                    2014, 10, 17, 13, 13, tzinfo=timezone('America/New_York')
                ),
                status='APPROVED',
                stats=Stats(
                    impressions=2798,
                    clicks=3,
                ),
                total_budget=Cost(
                    budget_micro_amount=10965060500000.0,
                    budget_currency_code='USD',
                ),
            ),
            Campaign(
                advertiser_id=self.TEST_ADVERTISER_ID,
                agency_id=None,
                creator_id='91002483',
                currency_code='USD',
                end=datetime(
                    2015, 8, 15, 23, 59, tzinfo=timezone('America/New_York')
                ),
                external_campaign_id='0',
                id='250057323',
                name='Blockbuster Sample Campaign (copy 1)',
                start=datetime(
                    2014, 11, 1, 0, 0, tzinfo=timezone('America/New_York')
                ),
                status='DRAFT',
                stats=Stats(
                    impressions=0,
                    clicks=0,
                ),
                total_budget=Cost(
                    budget_micro_amount=0.0,
                    budget_currency_code='USD',
                ),
            ),
            Campaign(
                advertiser_id=self.TEST_ADVERTISER_ID,
                agency_id=None,
                creator_id='125757723',
                currency_code='USD',
                end=datetime(
                    2015, 3, 6, 23, 59, tzinfo=timezone('America/New_York')
                ),
                external_campaign_id='0',
                id='288796443',
                name='Some Order',
                start=datetime(
                    2015, 3, 5, 13, 38, tzinfo=timezone('America/New_York')
                ),
                status='APPROVED',
                stats=Stats(
                    impressions=54,
                    clicks=0,
                ),
                total_budget=Cost(
                    budget_micro_amount=1000000.0,
                    budget_currency_code='USD',
                ),
            ),
        ])
        test_campaigns = set(self.parselmouth.get_campaigns(
            advertiserId=self.TEST_ADVERTISER_ID
        ))
        self.assertEqual(len(expected_campaigns), len(test_campaigns))
        self.assertSetEqual(expected_campaigns, test_campaigns)

    def test_get_campaign_line_items(self):
        expected_line_items = set(EXPECTED_LINE_ITEMS)
        test_campaign_line_items = set(
            self.parselmouth.get_campaign_line_items(
                self.TEST_CAMPAIGN_LINE_ITEMS
            )
        )
        self.assertSetEqual(expected_line_items, test_campaign_line_items)

    def test_bad_line_item(self):
        with self.assertRaises(ParselmouthException):
            _ = self.parselmouth.provider.get_line_item(self.BAD_LINE_ITEM_ID)

    def test_line_item(self):

        test_line_item = \
            self.parselmouth.provider.get_line_item(self.LINE_ITEM_ID)

        answer_line_item = LineItem(
            budget=Cost(
                budget_micro_amount=1000000000.0,
                budget_currency_code='USD',
            ),
            cost_per_unit=Cost(
                budget_micro_amount=100000000.0,
                budget_currency_code='USD',
            ),
            cost_type='CPM',
            delivery=DeliveryMeta(
                stats=Stats(
                    impressions=0,
                    clicks=0,
                ),
                delivery_rate_type='FRONTLOADED',
                actual_delivery_percent=0.0,
                expected_delivery_percent=0.0,
            ),
            end=datetime(
                2015, 8, 14, 23, 59, tzinfo=timezone('America/New_York')
            ),
            id='150163803',
            type='standard',
            name='Justin Test lineitem 1',
            campaign_id='287597403',
            campaign_name='Justins test campaign 1',
            primary_goal=Goal(
                goal_type='LIFETIME',
                unit_type='IMPRESSIONS',
                units=10000,
            ),
            start=datetime(
                2015, 3, 3, 15, 57, tzinfo=timezone('America/New_York')
            ),
            status='DRAFT',
            targeting=test_line_item.targeting,
            target_platform='ANY',
            value_cost_per_unit=Cost(
                budget_micro_amount=0.0,
                budget_currency_code='USD',
            ),
            creative_placeholder=[{
                'expectedCreativeCount': '1',
                'creativeSizeType': 'PIXEL',
                'size': {
                    'width': '300',
                    'isAspectRatio': False,
                    'height': '600'
                }
            }]
        )
        self.assertEqual(test_line_item, answer_line_item)

    def test_get_line_items(self):
        expected_line_items = set(EXPECTED_LINE_ITEMS)
        test_line_items = set(
            self.parselmouth.provider.get_line_items(
                orderId=self.TEST_CAMPAIGN_LINE_ITEMS
            )
        )
        self.assertSetEqual(expected_line_items, test_line_items)

    def test_get_line_item_creatives(self):
        expected_line_item_creatives = set([BLOCKBUSTER_728_CREATIVE])
        test_line_item_creatives = \
            set(self.parselmouth.get_line_item_creatives('132049083'))
        self.assertSetEqual(expected_line_item_creatives, test_line_item_creatives)

    def test_bad_creative(self):
        with self.assertRaises(ParselmouthException):
            _ = self.parselmouth.provider.get_creative(self.BAD_CREATIVE_ID)

    def test_get_creative(self):
        expected_creative = Creative(
            advertiser_id='57947163',
            id='48847852923',
            name='Blockbuster Total Access (300x250)',
            size={
                'height': '250',
                'isAspectRatio': False,
                'width': '300'
            },
        )
        test_creative = self.parselmouth.get_creative('48847852923')
        self.assertEqual(expected_creative, test_creative)

    def test_get_creatives(self):
        expected_creatives = set([
            BLOCKBUSTER_728_CREATIVE,
            Creative(
                advertiser_id='57947163',
                id='48847852923',
                name='Blockbuster Total Access (300x250)',
                size={
                    'height': '250',
                    'isAspectRatio': False,
                    'width': '300'
                },
            ),
            Creative(
                advertiser_id='57947163',
                id='60447694683',
                name='ad1',
                size={
                    'height': '90',
                    'isAspectRatio': False,
                    'width': '728'
                },
            ),
            Creative(
                advertiser_id='57947163',
                id='59188102683',
                name='iab research image',
                size={
                    'height': '90',
                    'isAspectRatio': False,
                    'width': '728'
                },
            ),
            Creative(
                advertiser_id= '57947163',
                id = '76601869803',
                name = 'abu blockbuster test ',
                size = {
                    'height': '250',
                    'isAspectRatio': False,
                    'width': '300'
                },
            ),
            Creative(
                advertiser_id = '57947163',
                id = '76562934243',
                name = 'Dynamic Logic Test 728x90',
                size = {
                    'height': '90',
                    'isAspectRatio': False,
                    'width': '728'
                },
            ),
            Creative(
                advertiser_id = '57947163',
                id = '75454103523',
                name = 'blockbuster 728x90 master',
                size = {
                    'height': '90',
                    'isAspectRatio': False,
                    'width': '728'
                },
            ),
            Creative(
                advertiser_id = '57947163',
                id = '75454135203',
                name = 'blockbuster 300x250 companion (copy)',
                size = {
                    'height': '90',
                    'isAspectRatio': False,
                    'width': '728'
                },
            ),
            Creative(
                advertiser_id = '57947163',
                id = '75454137843',
                name = '300x250 blockbuster roadblock test',
                size = {
                    'height': '250',
                    'isAspectRatio': False,
                    'width': '300'
                },
            ),
            Creative(
                advertiser_id = '57947163',
                id = '75454113123',
                name = 'blockbuster 300x250 companion',
                size = {
                    'height': '90',
                    'isAspectRatio': False,
                    'width': '728'
                },
            )
        ])
        test_creatives = set(
            self.parselmouth.get_creatives(
                advertiserId=self.TEST_ADVERTISER_ID
            )
        )
        self.assertSetEqual(expected_creatives, test_creatives)

    @unittest.skip("Test takes too long")
    def test_get_line_item_report(self):
        test_report = self.parselmouth.get_line_item_report(
            start=datetime(2015, 1, 1),
            end=datetime(2015, 1, 2),
            columns=['ad_impressions'],
        )
        expected_report = [
            {
                'line_item_name': 'Homepage 2x2',
                'line_item_id': '110849043',
                'ad_impressions': 822
            },
            {
                'line_item_name': 'Blockbuster Total Access (728x90)',
                'line_item_id': '132049083',
                'ad_impressions': 7
            },
            {
                'line_item_name': 'Circuit City 300x250 Annual',
                'line_item_id': '132159723',
                'ad_impressions': 2
            },
            {
                'line_item_name': 'Nathan\'s "Dog A Day" Winter Campaign 300x600',
                'line_item_id': '132160323',
                'ad_impressions': 6
            },
            {
                'line_item_name': 'Circuit City Fast & Furious (728x90)',
                'line_item_id': '132576963',
                'ad_impressions': 4
            },
            {
                'line_item_name': 'Blockbuster Total Access (300x250)',
                'line_item_id': '132581643',
                'ad_impressions': 3
            }
        ]
        self.assertListEqual(test_report, expected_report)

    def test_targeting(self):

        test_line_item = \
            self.parselmouth.provider.get_line_item(self.LINE_ITEM_ID)
        test_targeting_data = test_line_item.targeting

        dfp_inventory_target = {
            'targetedAdUnits': [{
                'includeDescendants': True,
                'adUnitId': '45282123',
            }],
        }
        answer_inventory_targeting = \
            transform_inventory_targeting_from_dfp(dfp_inventory_target)
        self.assertEqual(
            test_targeting_data.inventory,
            answer_inventory_targeting
        )

        dfp_custom_target = {
            'children': [{
                'children': [{
                    'operator': 'IS',
                    'keyId': '434163',
                    'valueIds': ['103142178723']
                }],
                'logicalOperator': 'AND',
            }],
            'logicalOperator': 'OR',
        }
        answer_custom_targeting = \
            transform_custom_targeting_from_dfp(dfp_custom_target)
        self.assertEqual(test_targeting_data.custom, answer_custom_targeting)

        answer_targeting_data = TargetingData(
            inventory=answer_inventory_targeting,
            geography=None,
            day_part=None,
            user_domain=None,
            technology=None,
            video_content=None,
            video_position=None,
            custom=answer_custom_targeting,
        )
        self.assertEqual(test_targeting_data, answer_targeting_data)

if __name__ == '__main__':
    unittest.main()
