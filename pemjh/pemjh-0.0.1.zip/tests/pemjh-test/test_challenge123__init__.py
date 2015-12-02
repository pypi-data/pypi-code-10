""" Tests for challenge123 """
from pemjh.challenge123 import challenge123
import pytest


@pytest.mark.regression
def test_challenge123():
    """ Regression testing challenge123 """
    assert challenge123() == 21035
