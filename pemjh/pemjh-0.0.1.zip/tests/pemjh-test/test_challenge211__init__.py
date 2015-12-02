""" Tests for challenge211 """
from pemjh.challenge211 import challenge211
import pytest


@pytest.mark.regression
def test_challenge211():
    """ Regression testing challenge211 """
    assert challenge211() == 1922364685
