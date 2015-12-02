""" Tests for challenge011 """
from pemjh.challenge011 import challenge011
import pytest


@pytest.mark.regression
def test_challenge011():
    """ Regression testing challenge011 """
    assert challenge011() == 70600674
