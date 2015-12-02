""" Tests for challenge131 """
from pemjh.challenge131 import challenge131
import pytest


@pytest.mark.regression
def test_challenge131():
    """ Regression testing challenge131 """
    assert challenge131() == 173
