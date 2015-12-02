""" Tests for challenge073 """
from pemjh.challenge073 import challenge073
import pytest


@pytest.mark.regression
def test_challenge073():
    """ Regression testing challenge073 """
    assert challenge073() == 5066251
