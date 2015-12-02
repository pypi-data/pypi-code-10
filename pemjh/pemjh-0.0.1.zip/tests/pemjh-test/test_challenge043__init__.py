""" Tests for challenge043 """
from pemjh.challenge043 import challenge043
import pytest


@pytest.mark.regression
def test_challenge043():
    """ Regression testing challenge043 """
    assert challenge043() == 16695334890
