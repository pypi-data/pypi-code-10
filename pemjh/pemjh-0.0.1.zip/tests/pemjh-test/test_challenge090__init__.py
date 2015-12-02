""" Tests for challenge090 """
from pemjh.challenge090 import challenge090
import pytest


@pytest.mark.regression
def test_challenge090():
    """ Regression testing challenge090 """
    assert challenge090() == 1217
