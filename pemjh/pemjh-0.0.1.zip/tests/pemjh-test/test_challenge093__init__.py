""" Tests for challenge093 """
from pemjh.challenge093 import challenge093
import pytest


@pytest.mark.regression
def test_challenge093():
    """ Regression testing challenge093 """
    assert challenge093() == 1258
