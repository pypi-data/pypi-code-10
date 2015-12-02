""" Tests for challenge138 """
from pemjh.challenge138 import challenge138
import pytest


@pytest.mark.regression
def test_challenge138():
    """ Regression testing challenge138 """
    assert challenge138() == 1118049290473932L
