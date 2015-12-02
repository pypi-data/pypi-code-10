""" Tests for challenge050 """
from pemjh.challenge050 import challenge050
import pytest


@pytest.mark.regression
def test_challenge050():
    """ Regression testing challenge050 """
    assert challenge050() == 997651
