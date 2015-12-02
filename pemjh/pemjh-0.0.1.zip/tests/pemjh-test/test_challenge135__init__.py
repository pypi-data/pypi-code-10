""" Tests for challenge135 """
from pemjh.challenge135 import challenge135
import pytest


@pytest.mark.regression
def test_challenge135():
    """ Regression testing challenge135 """
    assert challenge135() == 4989
