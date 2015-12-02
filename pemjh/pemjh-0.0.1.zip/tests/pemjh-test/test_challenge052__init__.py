""" Tests for challenge052 """
from pemjh.challenge052 import challenge052
import pytest


@pytest.mark.regression
def test_challenge052():
    """ Regression testing challenge052 """
    assert challenge052() == 142857
