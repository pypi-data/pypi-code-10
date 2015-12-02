""" Tests for challenge027 """
from pemjh.challenge027 import challenge027
import pytest


@pytest.mark.regression
def test_challenge027():
    """ Regression testing challenge027 """
    assert challenge027() == -59231
