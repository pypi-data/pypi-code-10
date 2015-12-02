""" Tests for challenge068 """
from pemjh.challenge068 import challenge068
import pytest


@pytest.mark.regression
def test_challenge068():
    """ Regression testing challenge068 """
    assert challenge068() == 6531031914842725L
