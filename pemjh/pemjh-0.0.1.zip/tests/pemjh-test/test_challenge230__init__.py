""" Tests for challenge230 """
from pemjh.challenge230 import challenge230
import pytest


@pytest.mark.regression
def test_challenge230():
    """ Regression testing challenge230 """
    assert challenge230() == 850481152593119296L
