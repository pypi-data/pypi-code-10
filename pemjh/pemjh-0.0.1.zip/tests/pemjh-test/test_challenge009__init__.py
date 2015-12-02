""" Tests for challenge009 """
from pemjh.challenge009 import challenge009
import pytest


@pytest.mark.regression
def test_challenge009():
    """ Regression testing challenge009 """
    assert challenge009() == 31875000
