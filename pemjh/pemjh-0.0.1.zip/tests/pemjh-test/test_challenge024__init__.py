""" Tests for challenge024 """
from pemjh.challenge024 import challenge024
import pytest


@pytest.mark.regression
def test_challenge024():
    """ Regression testing challenge024 """
    assert challenge024() == 2783915460L
