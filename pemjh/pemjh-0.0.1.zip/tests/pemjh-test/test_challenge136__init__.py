""" Tests for challenge136 """
from pemjh.challenge136 import challenge136
import pytest


@pytest.mark.regression
def test_challenge136():
    """ Regression testing challenge136 """
    assert challenge136() == 2544559
