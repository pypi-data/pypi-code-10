""" Tests for challenge190 """
from pemjh.challenge190 import challenge190
import pytest


@pytest.mark.regression
def test_challenge190():
    """ Regression testing challenge190 """
    assert challenge190() == 371048281
