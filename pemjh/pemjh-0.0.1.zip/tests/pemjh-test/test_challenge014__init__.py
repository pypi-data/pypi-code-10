""" Tests for challenge014 """
from pemjh.challenge014 import challenge014
import pytest


@pytest.mark.regression
def test_challenge014():
    """ Regression testing challenge014 """
    assert challenge014() == 837799
