""" Tests for challenge265 """
from pemjh.challenge265 import challenge265
import pytest


@pytest.mark.regression
def test_challenge265():
    """ Regression testing challenge265 """
    assert challenge265() == 209110240768L
