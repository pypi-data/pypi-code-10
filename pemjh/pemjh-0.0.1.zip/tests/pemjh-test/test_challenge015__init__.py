""" Tests for challenge015 """
from pemjh.challenge015 import challenge015
import pytest


@pytest.mark.regression
def test_challenge015():
    """ Regression testing challenge015 """
    assert challenge015() == 137846528820L
