""" Tests for challenge045 """
from pemjh.challenge045 import challenge045
import pytest


@pytest.mark.regression
def test_challenge045():
    """ Regression testing challenge045 """
    assert challenge045() == 1533776805L
