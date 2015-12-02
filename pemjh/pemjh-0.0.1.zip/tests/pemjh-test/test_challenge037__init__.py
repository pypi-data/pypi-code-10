""" Tests for challenge037 """
from pemjh.challenge037 import challenge037
import pytest


@pytest.mark.regression
def test_challenge037():
    """ Regression testing challenge037 """
    assert challenge037() == 748317
