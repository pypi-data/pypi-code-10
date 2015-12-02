""" Tests for challenge040 """
from pemjh.challenge040 import challenge040
import pytest


@pytest.mark.regression
def test_challenge040():
    """ Regression testing challenge040 """
    assert challenge040() == 210
