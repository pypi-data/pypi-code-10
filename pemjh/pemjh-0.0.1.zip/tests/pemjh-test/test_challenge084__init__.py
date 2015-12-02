""" Tests for challenge084 """
from pemjh.challenge084 import challenge084
import pytest


@pytest.mark.regression
def test_challenge084():
    """ Regression testing challenge084 """
    assert challenge084() == 101524
