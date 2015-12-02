""" Tests for challenge127 """
from pemjh.challenge127 import challenge127
import pytest


@pytest.mark.regression
def test_challenge127():
    """ Regression testing challenge127 """
    assert challenge127() == 18407904
