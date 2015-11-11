#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Rosetta Stone Test Harness

Contains inputs and outputs to test against
"""

# Future-proof
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Standard Library Imports
from datetime import datetime
from pytz import timezone

# Rosetta Stone Imports
from parselmouth.delivery import Cost
from parselmouth.delivery import Creative
from parselmouth.delivery import DeliveryMeta
from parselmouth.delivery import Goal
from parselmouth.delivery import LineItem
from parselmouth.delivery import Stats
from parselmouth.targeting import AdUnit
from parselmouth.targeting import TargetingCriterion
from parselmouth.targeting import TargetingData


CAMPAIGN_ID = '198816483'
EXPECTED_LINE_ITEMS = [
    LineItem(
        budget=Cost(
            budget_micro_amount=0.0,
            budget_currency_code='USD',
        ),
        cost_per_unit=Cost(
            budget_micro_amount=0.0,
            budget_currency_code='USD',
        ),
        cost_type='CPM',
        creative_placeholder=[{
            'creativeSizeType': 'PIXEL',
            'expectedCreativeCount': '1',
            'size': {
                'height': '768',
                'isAspectRatio': False,
                'width': '1024',
            }
        }],
        delivery=DeliveryMeta(
            actual_delivery_percent=0.0,
            delivery_rate_type='FRONTLOADED',
            expected_delivery_percent=0.0,
            stats=Stats(
                impressions=0,
                clicks=0,
            ),
        ),
        end=datetime(
            2014, 5, 31, 23, 59, tzinfo=timezone('America/New_York')
        ),
        id='112844283',
        name='Test Line Item',
        campaign_id=CAMPAIGN_ID,
        campaign_name='TestOrder (Do not modify)',
        primary_goal=Goal(
            goal_type='LIFETIME',
            unit_type='IMPRESSIONS',
            units=1000000,
        ),
        start=datetime(
            2014, 4, 23, 15, 50, tzinfo=timezone('America/New_York')
        ),
        status='DRAFT',
        targeting=TargetingData(
            custom=None,
            day_part=None,
            geography=None,
            inventory=TargetingCriterion(
                [AdUnit(id='30026763', include_descendants=True)],
                TargetingCriterion.OPERATOR.OR,
            ),
            user_domain=None,
            technology=None,
            video_content=None,
            video_position=None,
        ),
        target_platform='ANY',
        type='standard',
        value_cost_per_unit=Cost(
            budget_micro_amount=0.0,
            budget_currency_code='USD',
        ),
    ),
    LineItem(
        budget=Cost(
            budget_micro_amount=0.0,
            budget_currency_code='USD',
        ),
        cost_per_unit=Cost(
            budget_micro_amount=0.0,
            budget_currency_code='USD',
        ),
        cost_type='CPM',
        creative_placeholder=[{
            'creativeSizeType': 'PIXEL',
            'expectedCreativeCount': '1',
            'size': {
                'height': '100',
                'isAspectRatio': False,
                'width': '300',
            }
        }],
        delivery=DeliveryMeta(
            actual_delivery_percent=0.0,
            delivery_rate_type='FRONTLOADED',
            expected_delivery_percent=0.0,
            stats=Stats(
                impressions=0,
                clicks=0,
            ),
        ),
        end=datetime(
            2014, 12, 31, 23, 59, tzinfo=timezone('America/New_York')
        ),
        id='123281403',
        name='TestCreative',
        campaign_id=CAMPAIGN_ID,
        campaign_name='TestOrder (Do not modify)',
        primary_goal=Goal(
            goal_type='LIFETIME',
            unit_type='IMPRESSIONS',
            units=1000,
        ),
        start=datetime(
            2014, 7, 23, 19, 24, tzinfo=timezone('America/New_York')
        ),
        status='DRAFT',
        targeting=TargetingData(
            custom=None,
            day_part=None,
            geography=None,
            inventory=TargetingCriterion(
                [AdUnit(id='30026763', include_descendants=True)],
                TargetingCriterion.OPERATOR.OR,
            ),
            user_domain=None,
            technology=None,
            video_content=None,
            video_position=None,
        ),
        target_platform='ANY',
        type='standard',
        value_cost_per_unit=Cost(
            budget_micro_amount=0.0,
            budget_currency_code='USD',
        ),
    ),
]
BLOCKBUSTER_728_CREATIVE = Creative(
    advertiser_id='57947163',
    id='48847858203',
    name='Blockbuster Total Access (728x90)',
    preview_url=None,
    size={'height': '90', 'isAspectRatio': False, 'width': '728'},
)
