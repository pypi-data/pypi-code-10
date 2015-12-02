""" Tests for challenge132 """
from pemjh.challenge132 import challenge132
import pytest


@pytest.mark.regression
def test_challenge132():
    """ Regression testing challenge132 """
    assert challenge132() == 843296
