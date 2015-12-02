""" Tests for challenge096 """
from pemjh.challenge096 import challenge096
import pytest


@pytest.mark.regression
def test_challenge096():
    """ Regression testing challenge096 """
    assert challenge096() == 24702
