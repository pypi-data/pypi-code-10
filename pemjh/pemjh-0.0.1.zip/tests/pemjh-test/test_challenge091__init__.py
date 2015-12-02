""" Tests for challenge091 """
from pemjh.challenge091 import challenge091
import pytest


@pytest.mark.regression
def test_challenge091():
    """ Regression testing challenge091 """
    assert challenge091() == 14234
