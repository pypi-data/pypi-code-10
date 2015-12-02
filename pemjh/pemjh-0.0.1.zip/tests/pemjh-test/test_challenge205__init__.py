""" Tests for challenge205 """
from pemjh.challenge205 import challenge205
import pytest


@pytest.mark.regression
def test_challenge205():
    """ Regression testing challenge205 """
    assert challenge205() == 0.5731441
