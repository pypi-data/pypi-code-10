""" Tests for challenge035 """
from pemjh.challenge035 import challenge035
import pytest


@pytest.mark.regression
def test_challenge035():
    """ Regression testing challenge035 """
    assert challenge035() == 55
