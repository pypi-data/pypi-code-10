""" Tests for challenge063 """
from pemjh.challenge063 import challenge063
import pytest


@pytest.mark.regression
def test_challenge063():
    """ Regression testing challenge063 """
    assert challenge063() == 49
