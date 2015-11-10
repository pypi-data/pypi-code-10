import pytest

from .test_window import win
from hackedit.api import signals


@pytest.mark.parametrize('signal', signals.SIGNALS)
def test_connect_slot(qtbot, signal):
    def slot():
        pass
    win(qtbot)
    signals.connect_slot(signal, slot)
    signals.disconnect_slot(signal, slot)
