""" Tests for challenge106 """
from pemjh.challenge106 import challenge106
import pytest


@pytest.mark.regression
def test_challenge106():
    """ Regression testing challenge106 """
    assert challenge106() == 21384
