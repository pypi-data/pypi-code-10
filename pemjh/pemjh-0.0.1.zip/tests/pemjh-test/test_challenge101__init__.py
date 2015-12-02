""" Tests for challenge101 """
from pemjh.challenge101 import challenge101
import pytest


@pytest.mark.regression
def test_challenge101():
    """ Regression testing challenge101 """
    assert challenge101() == 37076114526L
