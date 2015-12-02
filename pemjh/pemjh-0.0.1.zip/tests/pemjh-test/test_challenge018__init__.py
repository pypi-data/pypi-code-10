""" Tests for challenge018 """
from pemjh.challenge018 import challenge018
import pytest


@pytest.mark.regression
def test_challenge018():
    """ Regression testing challenge018 """
    assert challenge018() == 1074
