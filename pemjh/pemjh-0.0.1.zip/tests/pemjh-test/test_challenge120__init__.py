""" Tests for challenge120 """
from pemjh.challenge120 import challenge120
import pytest


@pytest.mark.regression
def test_challenge120():
    """ Regression testing challenge120 """
    assert challenge120() == 333082500
