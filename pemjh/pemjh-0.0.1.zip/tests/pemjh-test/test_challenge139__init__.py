""" Tests for challenge139 """
from pemjh.challenge139 import challenge139
import pytest


@pytest.mark.regression
def test_challenge139():
    """ Regression testing challenge139 """
    assert challenge139() == 10057761
