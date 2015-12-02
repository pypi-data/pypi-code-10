""" Tests for challenge151 """
from pemjh.challenge151 import challenge151
import pytest


@pytest.mark.regression
def test_challenge151():
    """ Regression testing challenge151 """
    assert challenge151() == 0.464399
