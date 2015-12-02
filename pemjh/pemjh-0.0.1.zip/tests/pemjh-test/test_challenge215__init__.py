""" Tests for challenge215 """
from pemjh.challenge215 import challenge215
import pytest


@pytest.mark.regression
def test_challenge215():
    """ Regression testing challenge215 """
    assert challenge215() == 806844323190414L
