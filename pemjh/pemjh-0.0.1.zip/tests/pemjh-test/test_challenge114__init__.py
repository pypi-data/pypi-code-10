""" Tests for challenge114 """
from pemjh.challenge114 import challenge114
import pytest


@pytest.mark.regression
def test_challenge114():
    """ Regression testing challenge114 """
    assert challenge114() == 16475640049L
