""" Tests for challenge206 """
from pemjh.challenge206 import challenge206
import pytest


@pytest.mark.regression
def test_challenge206():
    """ Regression testing challenge206 """
    assert challenge206() == 1389019170
