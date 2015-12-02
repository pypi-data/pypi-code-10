""" Tests for challenge099 """
from pemjh.challenge099 import challenge099
import pytest


@pytest.mark.regression
def test_challenge099():
    """ Regression testing challenge099 """
    assert challenge099() == 709
