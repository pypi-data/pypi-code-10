""" Tests for challenge130 """
from pemjh.challenge130 import challenge130
import pytest


@pytest.mark.regression
def test_challenge130():
    """ Regression testing challenge130 """
    assert challenge130() == 149253
