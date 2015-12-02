""" Tests for challenge085 """
from pemjh.challenge085 import challenge085
import pytest


@pytest.mark.regression
def test_challenge085():
    """ Regression testing challenge085 """
    assert challenge085() == 2772
