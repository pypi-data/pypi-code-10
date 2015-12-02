""" Tests for challenge017 """
from pemjh.challenge017 import challenge017
import pytest


@pytest.mark.regression
def test_challenge017():
    """ Regression testing challenge017 """
    assert challenge017() == 21124
