""" Tests for challenge029 """
from pemjh.challenge029 import challenge029
import pytest


@pytest.mark.regression
def test_challenge029():
    """ Regression testing challenge029 """
    assert challenge029() == 9183
