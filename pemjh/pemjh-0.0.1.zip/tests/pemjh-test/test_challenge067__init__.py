""" Tests for challenge067 """
from pemjh.challenge067 import challenge067
import pytest


@pytest.mark.regression
def test_challenge067():
    """ Regression testing challenge067 """
    assert challenge067() == 7273
