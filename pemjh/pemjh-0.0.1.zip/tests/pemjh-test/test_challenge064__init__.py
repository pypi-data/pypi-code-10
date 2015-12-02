""" Tests for challenge064 """
from pemjh.challenge064 import challenge064
import pytest


@pytest.mark.regression
def test_challenge064():
    """ Regression testing challenge064 """
    assert challenge064() == 1322
