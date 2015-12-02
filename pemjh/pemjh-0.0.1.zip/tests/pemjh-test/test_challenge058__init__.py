""" Tests for challenge058 """
from pemjh.challenge058 import challenge058
import pytest


@pytest.mark.regression
def test_challenge058():
    """ Regression testing challenge058 """
    assert challenge058() == 26241
