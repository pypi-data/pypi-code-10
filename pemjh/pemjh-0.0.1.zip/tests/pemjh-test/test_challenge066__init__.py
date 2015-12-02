""" Tests for challenge066 """
from pemjh.challenge066 import challenge066
import pytest


@pytest.mark.regression
def test_challenge066():
    """ Regression testing challenge066 """
    assert challenge066() == 661
