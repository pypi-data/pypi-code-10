""" Tests for challenge107 """
from pemjh.challenge107 import challenge107
import pytest


@pytest.mark.regression
def test_challenge107():
    """ Regression testing challenge107 """
    assert challenge107() == 259679
