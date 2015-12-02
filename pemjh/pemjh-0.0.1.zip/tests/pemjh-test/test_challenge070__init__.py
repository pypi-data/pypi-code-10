""" Tests for challenge070 """
from pemjh.challenge070 import challenge070
import pytest


@pytest.mark.regression
def test_challenge070():
    """ Regression testing challenge070 """
    assert challenge070() == 8319823
