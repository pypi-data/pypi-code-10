""" Tests for challenge122 """
from pemjh.challenge122 import challenge122
import pytest


@pytest.mark.regression
def test_challenge122():
    """ Regression testing challenge122 """
    assert challenge122() == 1582
