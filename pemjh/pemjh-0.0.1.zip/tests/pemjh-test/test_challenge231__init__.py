""" Tests for challenge231 """
from pemjh.challenge231 import challenge231
import pytest


@pytest.mark.regression
def test_challenge231():
    """ Regression testing challenge231 """
    assert challenge231() == 7526965179680
