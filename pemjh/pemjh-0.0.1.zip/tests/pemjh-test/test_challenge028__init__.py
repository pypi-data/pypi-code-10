""" Tests for challenge028 """
from pemjh.challenge028 import challenge028
import pytest


@pytest.mark.regression
def test_challenge028():
    """ Regression testing challenge028 """
    assert challenge028() == 669171001
