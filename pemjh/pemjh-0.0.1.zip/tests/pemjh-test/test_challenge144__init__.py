""" Tests for challenge144 """
from pemjh.challenge144 import challenge144
import pytest


@pytest.mark.regression
def test_challenge144():
    """ Regression testing challenge144 """
    assert challenge144() == 354
