# Released under GPL3 terms (see LICENSE)

"""Special sleep functions"""

from . import io
import time

def sleep_roughly(seconds):
    """
    Instead of sleeping, for example, 1 second, target the start of the next
    second. This prevents skipping seconds when displaying the time like this:

        10:30:15.997
      +        1.000s sleep
      +        0.005s inaccuracy
      = 10:30:17.002  # Where's 10:30:16?

    But more importantly, it means every worker with update intervals can
    print at almost the exact same time, reducing the number of updates for
    i3bar.
    """
    now = time.time()
    target = int(now) + seconds + 0.01
    try:
        time.sleep(target - now)
    except KeyboardInterrupt:
        exit(0)

def sleep_til_midnight():
    """Sleep until the next day starts"""
    from datetime import (datetime, timedelta)
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    secs_till_midnight = (midnight - now).total_seconds()
    io.debug('Sleeping {} seconds from {} until midnight at {}'
             .format(secs_till_midnight, now.timestamp(), midnight.timestamp()))
    time.sleep(secs_till_midnight)

