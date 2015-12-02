""" Tests for challenge191 """
from pemjh.challenge191 import challenge191
import pytest


@pytest.mark.regression
def test_challenge191():
    """ Regression testing challenge191 """
    assert challenge191() == 1918080160L
