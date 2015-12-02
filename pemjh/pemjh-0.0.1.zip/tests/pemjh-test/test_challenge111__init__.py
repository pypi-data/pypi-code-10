""" Tests for challenge111 """
from pemjh.challenge111 import challenge111
import pytest


@pytest.mark.regression
def test_challenge111():
    """ Regression testing challenge111 """
    assert challenge111() == 612407567715L
