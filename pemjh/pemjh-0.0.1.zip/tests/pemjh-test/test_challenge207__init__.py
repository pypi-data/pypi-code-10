""" Tests for challenge207 """
from pemjh.challenge207 import challenge207
import pytest


@pytest.mark.regression
def test_challenge207():
    """ Regression testing challenge207 """
    assert challenge207() == 44043947822L
