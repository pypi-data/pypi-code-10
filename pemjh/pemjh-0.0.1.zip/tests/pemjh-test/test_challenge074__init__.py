""" Tests for challenge074 """
from pemjh.challenge074 import challenge074
import pytest


@pytest.mark.regression
def test_challenge074():
    """ Regression testing challenge074 """
    assert challenge074() == 402
