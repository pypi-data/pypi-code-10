""" Tests for challenge082 """
from pemjh.challenge082 import challenge082
import pytest


@pytest.mark.regression
def test_challenge082():
    """ Regression testing challenge082 """
    assert challenge082() == 260324
