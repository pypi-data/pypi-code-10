#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Acceptance checks to determine if DFP API responses are
compatible with the current dfp interface implementation
"""

# Standard Library Imports
import unittest

# Rosetta Stone Imports
from parselmouth import Parselmouth
from parselmouth import ParselmouthProviders
from parselmouth.targeting import TargetingData
from parselmouth.adapters.dfp.targeting_utils import transform_custom_targeting_from_dfp
from parselmouth.adapters.dfp.targeting_utils import transform_inventory_targeting_from_dfp


class TestApiResponse(unittest.TestCase):

    DOMAIN = 'ads.demo.com'
    CAMPAIGN_ID = '287597403'
    LINE_ITEM_ID = '150163803'

    def setUp(self):
        self.parselmouth = Parselmouth(
            provider_name=ParselmouthProviders.google_dfp_premium,
            config_path='dfp_integration_config.yaml',
        )

    def test_dfp_targeting(self):

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
