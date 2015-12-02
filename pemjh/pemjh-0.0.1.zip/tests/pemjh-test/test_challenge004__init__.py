""" Tests for challenge004 """
from pemjh.challenge004 import challenge004
import pytest


@pytest.mark.regression
def test_challenge004():
    """ Regression testing challenge004 """
    assert challenge004() == 906609
