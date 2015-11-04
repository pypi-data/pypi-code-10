import datetime
import email.utils
import time


def parse_cache_time(time_string):
    bits = {
        'y': datetime.timedelta(days=365),
        'd': datetime.timedelta(days=1),
        'h': datetime.timedelta(hours=1),
        'm': datetime.timedelta(minutes=1),
    }
    timedelta = datetime.timedelta()
    for time_bit in time_string.split(' '):
        bit = time_bit[-1]
        multiple = int(time_bit[:-1])
        timedelta = timedelta + bits[bit] * multiple
    return timedelta


def parse_rfc2822(time_string):
    time_tuple = email.utils.parsedate(time_string)
    timestamp = time.mktime(time_tuple)
    return datetime.datetime.fromtimestamp(timestamp)


def get_max_age(cache_control):
    for bit in cache_control.split(';'):
        try:
            key, value = bit.strip().split('=', 2)
            if key == 'max-age':
                return int(value)
        except ValueError:
            continue
    return None
