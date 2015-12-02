""" Tests for challenge125 """
from pemjh.challenge125 import challenge125
import pytest


@pytest.mark.regression
def test_challenge125():
    """ Regression testing challenge125 """
    assert challenge125() == 2906969179L
