""" Tests for challenge243 """
from pemjh.challenge243 import challenge243
import pytest


@pytest.mark.regression
def test_challenge243():
    """ Regression testing challenge243 """
    assert challenge243() == 892371480L
