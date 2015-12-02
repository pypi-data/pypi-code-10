""" Tests for challenge112 """
from pemjh.challenge112 import challenge112
import pytest


@pytest.mark.regression
def test_challenge112():
    """ Regression testing challenge112 """
    assert challenge112() == 1587000
