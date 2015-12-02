""" Tests for challenge001 """
from pemjh.challenge001 import challenge001
import pytest


@pytest.mark.regression
def test_challenge001():
    """ Regression testing challenge001 """
    assert challenge001() == 233168
