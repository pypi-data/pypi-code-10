""" Tests for challenge162 """
from pemjh.challenge162 import challenge162
import pytest


@pytest.mark.regression
def test_challenge162():
    """ Regression testing challenge162 """
    assert challenge162() == '3D58725572C62302'
