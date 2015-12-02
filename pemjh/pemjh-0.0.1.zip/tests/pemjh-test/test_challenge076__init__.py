""" Tests for challenge076 """
from pemjh.challenge076 import challenge076
import pytest


@pytest.mark.regression
def test_challenge076():
    """ Regression testing challenge076 """
    assert challenge076() == 190569291
