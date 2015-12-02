""" Tests for challenge062 """
from pemjh.challenge062 import challenge062
import pytest


@pytest.mark.regression
def test_challenge062():
    """ Regression testing challenge062 """
    assert challenge062() == 127035954683L
