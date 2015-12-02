""" Tests for challenge137 """
from pemjh.challenge137 import challenge137
import pytest


@pytest.mark.regression
def test_challenge137():
    """ Regression testing challenge137 """
    assert challenge137() == 1120149658760L
