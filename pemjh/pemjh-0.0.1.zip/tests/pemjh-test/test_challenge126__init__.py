""" Tests for challenge126 """
from pemjh.challenge126 import challenge126
import pytest


@pytest.mark.regression
def test_challenge126():
    """ Regression testing challenge126 """
    assert challenge126() == 18522
