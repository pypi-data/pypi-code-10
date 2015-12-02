""" Tests for challenge081 """
from pemjh.challenge081 import challenge081
import pytest


@pytest.mark.regression
def test_challenge081():
    """ Regression testing challenge081 """
    assert challenge081() == 427337
