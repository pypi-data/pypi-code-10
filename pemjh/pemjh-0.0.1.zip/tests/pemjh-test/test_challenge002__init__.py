""" Tests for challenge002 """
from pemjh.challenge002 import challenge002
import pytest


@pytest.mark.regression
def test_challenge002():
    """ Regression testing challenge002 """
    assert challenge002() == 4613732
