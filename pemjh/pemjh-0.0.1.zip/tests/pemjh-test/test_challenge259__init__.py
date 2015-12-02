""" Tests for challenge259 """
from pemjh.challenge259 import challenge259
import pytest


@pytest.mark.regression
def test_challenge259():
    """ Regression testing challenge259 """
    assert challenge259() == 20101196798
