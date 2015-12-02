""" Tests for challenge149 """
from pemjh.challenge149 import challenge149
import pytest


@pytest.mark.regression
def test_challenge149():
    """ Regression testing challenge149 """
    assert challenge149() == 52852124
