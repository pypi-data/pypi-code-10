""" Tests for challenge148 """
from pemjh.challenge148 import challenge148
import pytest


@pytest.mark.regression
def test_challenge148():
    """ Regression testing challenge148 """
    assert challenge148() == 2129970655314432L
