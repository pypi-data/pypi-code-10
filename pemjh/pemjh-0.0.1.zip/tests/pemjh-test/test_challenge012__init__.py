""" Tests for challenge012 """
from pemjh.challenge012 import challenge012
import pytest


@pytest.mark.regression
def test_challenge012():
    """ Regression testing challenge012 """
    assert challenge012() == 76576500
