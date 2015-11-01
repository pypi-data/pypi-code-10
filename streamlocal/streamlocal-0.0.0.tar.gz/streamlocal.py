from paramiko.message import Message
from paramiko.common import cMSG_CHANNEL_OPEN
from paramiko.channel import Channel
from paramiko.ssh_exception import SSHException

import time
import threading

def _open_channel(self,
                 kind,
                 path='',
                 modeinfo=None,
                 window_size=None,
                 max_packet_size=None,
                 timeout=None):
    if not self.active:
        raise SSHException('SSH session not active')
    timeout = 3600 if timeout is None else timeout
    self.lock.acquire()
    try:
        window_size = self._sanitize_window_size(window_size)
        max_packet_size = self._sanitize_packet_size(max_packet_size)
        chanid = self._next_channel()
        m = Message()
        m.add_byte(cMSG_CHANNEL_OPEN)
        m.add_string(kind)
        m.add_int(chanid)
        m.add_int(window_size)
        m.add_int(max_packet_size)
        m.add_string(path)
        m.add_string('localhost')
        m.add_int(0)
        chan = Channel(chanid)
        self._channels.put(chanid, chan)
        self.channel_events[chanid] = event = threading.Event()
        self.channels_seen[chanid] = True
        chan._set_transport(self)
        chan._set_window(window_size, max_packet_size)
    finally:
        self.lock.release()
    self._send_user_message(m)
    start_ts = time.time()
    while True:
        event.wait(0.1)
        if not self.active:
            e = self.get_exception()
            if e is None:
                e = SSHException('Unable to open channel.')
            raise e
        if event.is_set():
            break
        elif start_ts + timeout < time.time():
            raise SSHException('Timeout openning channel.')
    chan = self._channels.get(chanid)
    if chan is not None:
        return chan
    e = self.get_exception()
    if e is None:
        e = SSHException('Unable to open channel.')
    raise e


def direct(transport, path, window_size=None, max_packet_size=None, timeout=None):
    return _open_channel(transport, 'direct-streamlocal@openssh.com',
                         path, None, window_size, max_packet_size, timeout)


def forwarded(transport, path, window_size=None, max_packet_size=None, timeout=None):
    return _open_channel(transport, 'forwarded-streamlocal@openssh.com',
                         path, '', window_size, max_packet_size, timeout)
