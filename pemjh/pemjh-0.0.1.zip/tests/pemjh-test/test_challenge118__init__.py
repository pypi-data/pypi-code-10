""" Tests for challenge118 """
from pemjh.challenge118 import challenge118
import pytest


@pytest.mark.regression
def test_challenge118():
    """ Regression testing challenge118 """
    assert challenge118() == 44680
