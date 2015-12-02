""" Tests for challenge008 """
from pemjh.challenge008 import challenge008
import pytest


@pytest.mark.regression
def test_challenge008():
    """ Regression testing challenge008 """
    assert challenge008() == 40824
