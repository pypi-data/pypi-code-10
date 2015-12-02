""" Tests for challenge134 """
from pemjh.challenge134 import challenge134
import pytest


@pytest.mark.regression
def test_challenge134():
    """ Regression testing challenge134 """
    assert challenge134() == 18613426663617118L
