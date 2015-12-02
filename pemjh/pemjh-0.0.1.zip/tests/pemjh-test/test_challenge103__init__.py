""" Tests for challenge103 """
from pemjh.challenge103 import challenge103
import pytest


@pytest.mark.regression
def test_challenge103():
    """ Regression testing challenge103 """
    assert challenge103() == 20313839404245L
