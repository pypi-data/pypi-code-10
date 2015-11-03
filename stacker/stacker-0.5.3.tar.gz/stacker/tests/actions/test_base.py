import unittest

from stacker.actions.base import get_stack_execution_order


def before(l, a, b):
    """Returns true if a is in l before b."""
    return l.index(a) < l.index(b)


class TestBefore(unittest.TestCase):
    def test_before(self):
        l = ['a', 'b', 'c']
        self.assertTrue(before(l, 'a', 'c'))
        self.assertTrue(before(l, 'b', 'c'))
        self.assertFalse(before(l, 'c', 'a'))
        self.assertFalse(before(l, 'c', 'b'))


class TestBaseAction(unittest.TestCase):
    def test_get_stack_execution_order(self):
        d = {
            'vpc': [],
            'bastion': ['vpc'],
            'nat': ['vpc'],
            'db': ['vpc', 'web'],
            'web': ['bastion']
        }

        r = get_stack_execution_order(d)
        self.assertTrue(before(r, 'vpc', 'web'))
        self.assertTrue(before(r, 'vpc', 'bastion'))
        self.assertTrue(before(r, 'vpc', 'nat'))
        self.assertTrue(before(r, 'bastion', 'web'))
        self.assertTrue(before(r, 'web', 'db'))
        self.assertTrue(before(r, 'vpc', 'db'))
        self.assertTrue(before(r, 'bastion', 'db'))
