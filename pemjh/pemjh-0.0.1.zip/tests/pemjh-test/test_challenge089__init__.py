""" Tests for challenge089 """
from pemjh.challenge089 import challenge089
import pytest


@pytest.mark.regression
def test_challenge089():
    """ Regression testing challenge089 """
    assert challenge089() == 743
