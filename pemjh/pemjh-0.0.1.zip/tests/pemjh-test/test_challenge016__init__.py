""" Tests for challenge016 """
from pemjh.challenge016 import challenge016
import pytest


@pytest.mark.regression
def test_challenge016():
    """ Regression testing challenge016 """
    assert challenge016() == 1366
