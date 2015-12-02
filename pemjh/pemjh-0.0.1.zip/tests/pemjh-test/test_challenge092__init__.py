""" Tests for challenge092 """
from pemjh.challenge092 import challenge092
import pytest


@pytest.mark.regression
def test_challenge092():
    """ Regression testing challenge092 """
    assert challenge092() == 8581146
