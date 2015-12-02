""" Tests for challenge145 """
from pemjh.challenge145 import challenge145
import pytest


@pytest.mark.regression
def test_challenge145():
    """ Regression testing challenge145 """
    assert challenge145() == 608720
