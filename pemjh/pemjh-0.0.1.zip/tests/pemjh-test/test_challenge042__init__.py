""" Tests for challenge042 """
from pemjh.challenge042 import challenge042
import pytest


@pytest.mark.regression
def test_challenge042():
    """ Regression testing challenge042 """
    assert challenge042() == 162
