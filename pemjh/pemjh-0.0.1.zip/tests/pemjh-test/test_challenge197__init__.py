""" Tests for challenge197 """
from pemjh.challenge197 import challenge197
import pytest


@pytest.mark.regression
def test_challenge197():
    """ Regression testing challenge197 """
    assert challenge197() == 1.710637717
