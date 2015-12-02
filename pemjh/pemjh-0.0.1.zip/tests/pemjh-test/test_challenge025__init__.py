""" Tests for challenge025 """
from pemjh.challenge025 import challenge025
import pytest


@pytest.mark.regression
def test_challenge025():
    """ Regression testing challenge025 """
    assert challenge025() == 4782
