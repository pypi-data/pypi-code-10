""" Tests for challenge022 """
from pemjh.challenge022 import challenge022
import pytest


@pytest.mark.regression
def test_challenge022():
    """ Regression testing challenge022 """
    assert challenge022() == 871198282
