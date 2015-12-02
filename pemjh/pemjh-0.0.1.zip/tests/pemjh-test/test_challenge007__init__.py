""" Tests for challenge007 """
from pemjh.challenge007 import challenge007
import pytest


@pytest.mark.regression
def test_challenge007():
    """ Regression testing challenge007 """
    assert challenge007() == 104743
