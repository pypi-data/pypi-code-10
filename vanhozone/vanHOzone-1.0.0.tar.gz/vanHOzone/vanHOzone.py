# The MIT License (MIT)
#
# Copyright (c) 2015 Robin Wilson (robin@rtwilson.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import numpy as np
from dateutil.parser import parse


def get_ozone_conc(lat, lon, timestamp):
    """
    Returns the ozone contents in matm-cm for the given latitude/longitude
    and timestamp (provided as either a datetime object or a string in any
    sensible format - I strongly recommend using an ISO 8601 format of
    yyyy-mm-dd) according to van Heuklon's Ozone model.

    The model is described in Van Heuklon, T. K. (1979). Estimating atmospheric
    ozone for solar radiation models. Solar Energy, 22(1), 63-68.

    This function uses numpy functions, so you can pass arrays and it will
    return an array of results. The timestamp argument can be either an
    array/list or a single value. If it is a single value then this will be
    used for all lat/lon values given.
    """
    # Deal with scalar values
    try:
        lat_count = len(lat)
    except:
        lat = [lat]
        lat_count = 1

    try:
        lon_count = len(lon)
    except:
        lon = [lon]
        lon_count = 1

    if lat_count != lon_count:
        raise ValueError("lan and lon arrays must be the same length")

    lat = np.array(lat)
    lon = np.array(lon)

    # Set the Day of Year
    try:
        # Try and do list-based things with it
        # If it works then it is a list, so check length is correct
        # and process
        count = len(timestamp)
        if count == len(lat):
            try:
                E = [t.timetuple().tm_yday for t in timestamp]
                E = np.array(E)
            except:
                d = [parse(t) for t in timestamp]
                E = [dt.timetuple().tm_yday for dt in d]
                E = np.array(E)
        else:
            raise ValueError("Timestamp must be the same length as lat and lon")
    except:
        # It isn't a list, so just do it once
        try:
            # If this works then it is a datetime obj
            E = timestamp.timetuple().tm_yday
        except:
            # If not then a string, so parse it and set it
            d = parse(timestamp)
            E = d.timetuple().tm_yday

    # Set parameters which are the same for both
    # hemispheres
    D = 0.9865
    G = 20.0
    J = 235.0

    # Set to Northern Hemisphere values by default
    A = np.zeros(np.shape(lat)) + 150.0
    B = np.zeros(np.shape(lat)) + 1.28
    C = np.zeros(np.shape(lat)) + 40.0
    F = np.zeros(np.shape(lat)) - 30.0
    H = np.zeros(np.shape(lat)) + 3.0
    I = np.zeros(np.shape(lat))

    # Gives us a boolean array indicating
    # which indices are below the equator
    # which we can then use for indexing below
    southern = lat < 0

    A[southern] = 100.0
    B[southern] = 1.5
    C[southern] = 30.0
    F[southern] = 152.625
    H[southern] = 2.0
    I[southern] = -75.0

    # Set all northern I values to 20.0
    # (the northern indices are the inverse (~) of
    # the southern indices)
    I[~southern] = 20.0

    I[(~southern) & (lon <= 0)] = 0.0

    bracket = (A + (C * np.sin(np.radians(D * (E + F))) + G *
                    np.sin(np.radians(H * (lon + I)))))

    sine_bit = np.sin(np.radians(B * lat))
    sine_bit = sine_bit ** 2

    result = J + (bracket * sine_bit)

    return result
