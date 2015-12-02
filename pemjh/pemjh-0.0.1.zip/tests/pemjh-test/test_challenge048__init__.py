""" Tests for challenge048 """
from pemjh.challenge048 import challenge048
import pytest


@pytest.mark.regression
def test_challenge048():
    """ Regression testing challenge048 """
    assert challenge048() == 9110846700L
