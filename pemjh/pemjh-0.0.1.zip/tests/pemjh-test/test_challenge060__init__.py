""" Tests for challenge060 """
from pemjh.challenge060 import challenge060
import pytest


@pytest.mark.regression
def test_challenge060():
    """ Regression testing challenge060 """
    assert challenge060() == 26033
