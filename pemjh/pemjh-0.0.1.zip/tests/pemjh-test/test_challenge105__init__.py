""" Tests for challenge105 """
from pemjh.challenge105 import challenge105
import pytest


@pytest.mark.regression
def test_challenge105():
    """ Regression testing challenge105 """
    assert challenge105() == 73702
