""" Tests for challenge104 """
from pemjh.challenge104 import challenge104
import pytest


@pytest.mark.regression
def test_challenge104():
    """ Regression testing challenge104 """
    assert challenge104() == 329468
