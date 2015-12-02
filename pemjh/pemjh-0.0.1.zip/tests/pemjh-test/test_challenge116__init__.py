""" Tests for challenge116 """
from pemjh.challenge116 import challenge116
import pytest


@pytest.mark.regression
def test_challenge116():
    """ Regression testing challenge116 """
    assert challenge116() == 20492570929L
