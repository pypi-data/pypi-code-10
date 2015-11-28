import datetime
import pytz


def nowUtc():
    return datetime.datetime.now(tz=pytz.utc)
