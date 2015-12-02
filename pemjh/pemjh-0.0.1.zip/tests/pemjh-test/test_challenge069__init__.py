""" Tests for challenge069 """
from pemjh.challenge069 import challenge069
import pytest


@pytest.mark.regression
def test_challenge069():
    """ Regression testing challenge069 """
    assert challenge069() == 510510
