""" Tests for challenge187 """
from pemjh.challenge187 import challenge187
import pytest


@pytest.mark.regression
def test_challenge187():
    """ Regression testing challenge187 """
    assert challenge187() == 17427258
