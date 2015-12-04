
import numpy as np
import pandas as pd
import datetime
import dateutil.parser as dp

def extract_date(date_input, to_pandas=True):
    '''
    Converts any date input into a *datetime* object

    Parameters
    ----------
    date_input : int(s), float(s), or string(s)

    Returns
    -------
    date : *datetime* object(s)

    '''
    if isinstance(date_input, (list, pd.core.series.Series, np.ndarray)):
        return [extract_date(d, to_pandas=to_pandas) for d in date_input]

    if isinstance(date_input, (int, float)):
        if pd.isnull(date_input):
            return np.nan

    date = from_unixtime(date_input)
    if isinstance(date, datetime.datetime) == False:
        date = dp.parse(str(date), fuzzy=True)

    if to_pandas:
        date = pd.to_datetime(date)
    return date

def from_unixtime(date_input):
    '''
    Given a unix timestamp in seconds, milliseconds, microseconds, or nanoseconds from 1-Jan-1970:
    returns a datetime.datetime object.
    If the timestamp is not covertable to float, the method will pass and return the input as given

    Parameters
    ----------
    date_input : int, float, or string

    Returns
    -------
    date : *datetime* object

    '''
    try:
        timestamp = float(timestamp)
        digits = number.count_digits(timestamp)
        if digits <= 5:
            # convert excel date to datetime
            base = datetime.datetime(1900, 1, 1)
            delta = datetime.timedelta(days=timestamp)
            timestamp = base + delta
        else:
            base = datetime.datetime(1970, 1, 1)

            if (digits > 5) and (digits <= 10):
                # convert from seconds
                timestamp_s = timestamp

            elif (digits > 10) and (digits <= 13):
                # convert from milla-seconds
                timestamp_s = timestamp * 1e-3

            elif (digits > 13) and (digits <= 16):
                # convert from micro-seconds
                timestamp_s = timestamp * 1e-6
            elif (digits > 16) and (digits <= 19):
                # is already nanoseconds
                timestamp_s = timestamp * 1e-9

            delta = datetime.timedelta(seconds=timestamp_s)
            date = base + delta
    except:
        pass
    return date
