# -*- coding:utf-8 -*-
#
# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import testtools

import bandit
from bandit.core import issue
from bandit.core import constants


class IssueTests(testtools.TestCase):

    def test_issue_create(self):
        new_issue = _get_issue_instance()
        self.assertIsInstance(new_issue, issue.Issue)

    def test_issue_str(self):
        test_issue = _get_issue_instance()
        self.assertEqual(
            ("Issue: 'Test issue' from bandit_plugin: Severity: MEDIUM "
             "Confidence: MEDIUM at code.py:1"),
            str(test_issue)
        )

    def test_issue_as_dict(self):
        test_issue = _get_issue_instance()
        test_issue_dict = test_issue.as_dict(with_code=False)
        self.assertIsInstance(test_issue_dict, dict)
        self.assertEqual(test_issue_dict['filename'], 'code.py')
        self.assertEqual(test_issue_dict['test_name'], 'bandit_plugin')
        self.assertEqual(test_issue_dict['issue_severity'], 'MEDIUM')
        self.assertEqual(test_issue_dict['issue_confidence'], 'MEDIUM')
        self.assertEqual(test_issue_dict['issue_text'], 'Test issue')
        self.assertEqual(test_issue_dict['line_number'], 1)
        self.assertEqual(test_issue_dict['line_range'], [])

    def test_issue_filter_severity(self):
        levels = [bandit.LOW, bandit.MEDIUM, bandit.HIGH]
        issues = [_get_issue_instance(l, bandit.HIGH) for l in levels]

        for level in levels:
            rank = constants.RANKING.index(level)
            for issue in issues:
                test = constants.RANKING.index(issue.severity)
                result = issue.filter(level, bandit.UNDEFINED)
                self.assertTrue((test >= rank) == result)


    def test_issue_filter_confidence(self):
        levels = [bandit.LOW, bandit.MEDIUM, bandit.HIGH]
        issues = [_get_issue_instance(bandit.HIGH, l) for l in levels]

        for level in levels:
            rank = constants.RANKING.index(level)
            for issue in issues:
                test = constants.RANKING.index(issue.confidence)
                result = issue.filter(bandit.UNDEFINED, level)
                self.assertTrue((test >= rank) == result)



def _get_issue_instance(severity=bandit.MEDIUM, confidence=bandit.MEDIUM):
    new_issue = issue.Issue(severity, confidence, 'Test issue')
    new_issue.fname = 'code.py'
    new_issue.test = 'bandit_plugin'
    new_issue.lineno = 1
    return new_issue
