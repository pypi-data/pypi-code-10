""" Tests for challenge204 """
from pemjh.challenge204 import challenge204
import pytest


@pytest.mark.regression
def test_challenge204():
    """ Regression testing challenge204 """
    assert challenge204() == 2944730
