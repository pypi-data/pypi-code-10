""" Tests for challenge020 """
from pemjh.challenge020 import challenge020
import pytest


@pytest.mark.regression
def test_challenge020():
    """ Regression testing challenge020 """
    assert challenge020() == 648
