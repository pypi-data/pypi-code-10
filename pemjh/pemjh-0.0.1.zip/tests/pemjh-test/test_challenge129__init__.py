""" Tests for challenge129 """
from pemjh.challenge129 import challenge129
import pytest


@pytest.mark.regression
def test_challenge129():
    """ Regression testing challenge129 """
    assert challenge129() == 1000023
