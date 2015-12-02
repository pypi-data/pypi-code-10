""" Tests for challenge179 """
from pemjh.challenge179 import challenge179
import pytest


@pytest.mark.regression
def test_challenge179():
    """ Regression testing challenge179 """
    assert challenge179() == 986262
