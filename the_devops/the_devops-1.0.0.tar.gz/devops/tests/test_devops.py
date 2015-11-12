#!/usr/bin/python

"""
This class tests 'the devops' class.

This is reasonably proper! Whoop!
"""

import unittest
from devops.devops import devops

TEST_THE_DEVOPS = "Dude, you totally devopsificated"


class TestDevOps(unittest.TestCase):

    """DevOps object. Doesn't do anything other than the devops magic."""

    def setUp(self):
        self.thedevops = devops()
        pass

    def tearDown(self):
        pass

    def test_devops(self):
        """
        The test_devops method tests 'the devops'.

        Init:       Object init for DevOps
        Requires:   n/a
        Returns:    n/a
        Raises:     n/a
        """
        self.assertEqual(TEST_THE_DEVOPS, self.thedevops.__str__())


if __name__ == '__main__':
    unittest.main()
