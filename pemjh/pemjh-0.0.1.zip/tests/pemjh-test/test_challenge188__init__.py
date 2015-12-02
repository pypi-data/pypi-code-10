""" Tests for challenge188 """
from pemjh.challenge188 import challenge188
import pytest


@pytest.mark.regression
def test_challenge188():
    """ Regression testing challenge188 """
    assert challenge188() == 95962097L
