""" Tests for challenge054 """
from pemjh.challenge054 import challenge054
import pytest


@pytest.mark.regression
def test_challenge054():
    """ Regression testing challenge054 """
    assert challenge054() == 376
