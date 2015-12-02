""" Tests for challenge110 """
from pemjh.challenge110 import challenge110
import pytest


@pytest.mark.regression
def test_challenge110():
    """ Regression testing challenge110 """
    assert challenge110() == 9350130049860600L
