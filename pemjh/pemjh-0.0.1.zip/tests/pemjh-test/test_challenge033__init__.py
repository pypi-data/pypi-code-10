""" Tests for challenge033 """
from pemjh.challenge033 import challenge033
import pytest


@pytest.mark.regression
def test_challenge033():
    """ Regression testing challenge033 """
    assert challenge033() == 100
