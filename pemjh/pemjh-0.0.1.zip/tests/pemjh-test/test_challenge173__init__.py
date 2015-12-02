""" Tests for challenge173 """
from pemjh.challenge173 import challenge173
import pytest


@pytest.mark.regression
def test_challenge173():
    """ Regression testing challenge173 """
    assert challenge173() == 1572729
