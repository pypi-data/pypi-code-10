""" Tests for challenge049 """
from pemjh.challenge049 import challenge049
import pytest


@pytest.mark.regression
def test_challenge049():
    """ Regression testing challenge049 """
    assert challenge049() == 296962999629L
