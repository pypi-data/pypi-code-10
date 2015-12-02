""" Tests for challenge113 """
from pemjh.challenge113 import challenge113
import pytest


@pytest.mark.regression
def test_challenge113():
    """ Regression testing challenge113 """
    assert challenge113() == 51161058134250L
