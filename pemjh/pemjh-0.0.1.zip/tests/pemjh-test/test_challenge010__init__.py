""" Tests for challenge010 """
from pemjh.challenge010 import challenge010
import pytest


@pytest.mark.regression
def test_challenge010():
    """ Regression testing challenge010 """
    assert challenge010() == 142913828922L
