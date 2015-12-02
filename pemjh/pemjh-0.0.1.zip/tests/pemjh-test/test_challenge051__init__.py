""" Tests for challenge051 """
from pemjh.challenge051 import challenge051
import pytest


@pytest.mark.regression
def test_challenge051():
    """ Regression testing challenge051 """
    assert challenge051() == 121313
