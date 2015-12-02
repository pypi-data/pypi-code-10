""" Tests for challenge030 """
from pemjh.challenge030 import challenge030
import pytest


@pytest.mark.regression
def test_challenge030():
    """ Regression testing challenge030 """
    assert challenge030() == 443840
