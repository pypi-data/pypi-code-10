""" Tests for challenge077 """
from pemjh.challenge077 import challenge077
import pytest


@pytest.mark.regression
def test_challenge077():
    """ Regression testing challenge077 """
    assert challenge077() == 71
