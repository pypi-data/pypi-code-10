# Released under GPL3 terms (see LICENSE)

"""Provide information about network devices (needs psutil)"""

from . import (io, rate, cache)
import subprocess
import shlex
try:
    import psutil as _psutil
except ImportError:
    croak('Please install python3-psutil')

_nic_rates = {}
_nic_rates_avg = {}

@cache.timeout(seconds=0.1)
def get_byterate(nic, direction, samples=1):
    """
    Return current byte throughput of network interface `nic`

    `nic` is the name of the network interface (e.g. 'eth0')
    `direction` must be 'up' or 'down'
    `samples` is the number of past values to compute the average
    """
    try:
        counters = _psutil.net_io_counters(pernic=True)
    except NotADirectoryError as e:
        # TODO: Very rarely (maybe once a week) this exception is raised:
        # Traceback (most recent call last):
        #   File "/home/ich/.config/i3barfodder/scripts/netload", line 106, in <module>
        #     rate = get_rate()
        #   File "/home/ich/.config/i3barfodder/scripts/netload", line 72, in <lambda>
        #     get_rate = lambda: network.get_byterate(NIC, DIRECTION, SAMPLES) * 8
        #   File "/home/ich/code/i3barfodder/contrib/i3barinfo/utils.py", line 153, in wrapped
        #     self._returnvalues[callid] = func(*args, **kwargs)
        #   File "/home/ich/code/i3barfodder/contrib/i3barinfo/network.py", line 24, in get_byterate
        #     counters = psutil.net_io_counters(pernic=True)
        #   File "/usr/lib/python3/dist-packages/psutil/__init__.py", line 1784, in net_io_counters
        #     rawdict = _psplatform.net_io_counters()
        #   File "/usr/lib/python3/dist-packages/psutil/_pslinux.py", line 537, in net_io_counters
        #     with open("/proc/net/dev", "rt") as f:
        # NotADirectoryError: [Errno 20] Not a directory: '/proc/net/dev'

        # Simply insisting seems to work, though.
        counters = _psutil.net_io_counters(pernic=True)

    if nic not in counters:
        io.croak('Unknown NIC: {}'.format(nic))
    else:
        if nic not in _nic_rates:
            _nic_rates[nic] = { 'up': rate.RatePerSecond(),
                                'down': rate.RatePerSecond() }
            _nic_rates_avg[nic] = { 'up': rate.Average(samples),
                                    'down': rate.Average(samples) }

        if direction == 'down':
            current_value = counters[nic].bytes_recv
        elif direction == 'up':
            current_value = counters[nic].bytes_sent
        else:
            io.croak('Invalid direction: {!r}'.format(direction))

        rps = _nic_rates[nic][direction]
        avg = _nic_rates_avg[nic][direction]
        current_rate = rps.update(current_value)
        current_rate_avg = avg.update(current_rate)
        return int(current_rate_avg)


def get_default_nic():
    """Return the name of the default NIC according to 'ip route | grep ^default'"""
    cmd = 'ip route'
    try:
        lines = subprocess.check_output(shlex.split(cmd),
                                        universal_newlines=True).split('\n')
    except Exception as e:
        io.croak('Unable to auto-detect default NIC: '
                 'Running "{}" failed: {}'.format(cmd, e))

    for line in lines:
        if line.startswith('default'):
            try:
                start = line.index('dev ') + 4
            except ValueError:
                io.croak('No NIC found for default route: {}'.format(line))

            try:
                end = line[start:].index(' ') + start
            except ValueError:
                end = len(line)-1
            nic = line[start:end]
            io.debug('Auto-detected default NIC: {}'.format(nic))
            return nic

    io.croak('No default route in output of "ip route" found:\n' + \
             '\n'.join(lines))
