__author__ = 'cjoakim'
__version__ = '0.1.0'

"""
m26 library
"""

VERSION = __version__

import arrow
import math

from numbers import Number


class Age(object):
    """
    Instances of this class represent the age of a person, as a float value
    of their age in years.
    """
    def __init__(self, n=0.0):
        self.value = float(n)

    def max_pulse(self):
        if self.value < 20:
            return 200.0
        else:
            return 220.0 - self.value

    def add(self, another_instance):
        if another_instance:
            self.value = self.value + another_instance.value
        return self.value

    def subtract(self, another_instance):
        if another_instance:
            self.value = self.value - another_instance.value
        return self.value

    def training_zones(self):
        results = list()
        zones = [0.95, 0.90, 0.85, 0.80, 0.75]
        for idx, pct in enumerate(zones):
            data = dict()
            data['zone'] = idx + 1
            data['age'] = self.value
            data['max'] = self.max_pulse()
            data['pct_max'] = pct
            data['pulse'] = self.max_pulse() * pct
            results.append(data)
        return results

    def __str__(self):
        return "<Age value:{0}>".format(self.value)

    def __repr__(self):
        return self.__str__()


class AgeCalculator(object):

    @classmethod
    def seconds_per_year(cls):
        # seconds * minutes * hours * days
        return float(60 * 60 * 24 * 365.25)

    @classmethod
    def milliseconds_per_year(cls):
        return float(cls.seconds_per_year() * 1000.0)

    @classmethod
    def calculate(self, birth_yyyy_mm_dd, as_of_yyyy_mm_dd):
        if birth_yyyy_mm_dd:
            birth_date = arrow.get(birth_yyyy_mm_dd, 'YYYY-MM-DD')
            asof_date = arrow.get(as_of_yyyy_mm_dd, 'YYYY-MM-DD')
            if birth_date and asof_date:
                birth_ts = birth_date.timestamp
                asof_ts = asof_date.timestamp
                diff = float(asof_ts - birth_ts)
                years = diff / self.seconds_per_year()
                return Age(years)
        else:
            return None


class Constants(object):

    @classmethod
    def uom_miles(cls):
        return 'm'

    @classmethod
    def uom_kilometers(cls):
        return 'k'

    @classmethod
    def uom_yards(cls):
        return 'y'

    @classmethod
    def units_of_measure(cls):
        return ('m', 'k', 'y')

    @classmethod
    def kilometers_per_mile(cls):
        return float(1.609344)

    @classmethod
    def miles_per_kilometer(cls):
        return float(0.621371192237334)

    @classmethod
    def yards_per_kilometer(cls):
        return float(1093.6132983377076)

    @classmethod
    def feet_per_kilometer(cls):
        return float(3280.839895013123)

    @classmethod
    def feet_per_meter(cls):
        return float(3.280839895013123)

    @classmethod
    def yards_per_mile(cls):
        return float(1760.0)

    @classmethod
    def seconds_per_hour(cls):
        return float(3600.0)

    @classmethod
    def miles_per_marathon(cls):
        return float(26.2)


class Distance(object):

    def __init__(self, dist=0.0, uom=Constants.uom_miles()):
        self.value = float(dist)
        self.uom = self.unit_of_measure(uom)

    def unit_of_measure(self, s):
        u = str(s).strip().lower()
        if u == 'k':
            return Constants.uom_kilometers()
        elif u == 'y':
            return Constants.uom_yards()
        else:
            return Constants.uom_miles()

    def is_miles(self):
        return self.uom == Constants.uom_miles()

    def is_kilometers(self):
        return self.uom == Constants.uom_kilometers()

    def is_yards(self):
        return self.uom == Constants.uom_yards()

    def as_miles(self):
        if self.is_miles():
            return self.value
        elif self.is_kilometers():
            return self.value / Constants.kilometers_per_mile()
        else:
            return self.value / Constants.yards_per_mile()

    def as_kilometers(self):
        if self.is_miles():
            return self.value * Constants.kilometers_per_mile()
        elif self.is_kilometers():
            return self.value
        else:
            return self.value / Constants.yards_per_kilometer()

    def as_yards(self):
        if self.is_miles():
            return self.value * Constants.yards_per_mile()
        elif self.is_kilometers():
            return self.value * Constants.yards_per_kilometer()
        else:
            return self.value

    def add(self, another_instance):
        if self.is_miles():
            self.value = self.value + another_instance.as_miles()
        elif self.is_kilometers():
            self.value = self.value + another_instance.as_kilometers()
        else:
            self.value = self.value + another_instance.as_yards()

    def subtract(self, another_instance):
        if self.is_miles():
            self.value = self.value - another_instance.as_miles()
        elif self.is_kilometers():
            self.value = self.value - another_instance.as_kilometers()
        else:
            self.value = self.value - another_instance.as_yards()

    def __str__(self):
        return "<Distance value:{0} uom:{1}>".format(self.value, self.uom)

    def __repr__(self):
        return self.__str__()


class ElapsedTime(object):

    def __init__(self, val):
        self.secs = 0
        self.hh = 0
        self.mm = 0
        self.ss = 0

        if not val:
            val = 0
        if isinstance(val, Number):
            self.initialize_from_number(val)
        elif isinstance(val, str):
            self.initialize_from_string(val)

    def initialize_from_number(self, val):
        sph = Constants.seconds_per_hour()
        self.secs = float(val)
        self.hh = math.floor(self.secs / sph)
        rem = self.secs - (self.hh * sph)
        self.mm = math.floor(rem / 60.0)
        self.ss = rem - (self.mm * 60.0)

    def initialize_from_string(self, val):
        stripped = str(val).strip()
        if len(stripped) > 0:
            tokens = stripped.split(':')
            if len(tokens) == 0:
                pass
            elif len(tokens) == 1:
                self.ss = self.to_float(tokens[0])
            elif len(tokens) == 2:
                self.mm = self.to_float(tokens[0])
                self.ss = self.to_float(tokens[1])
            elif len(tokens) == 3:
                self.hh = self.to_float(tokens[0])
                self.mm = self.to_float(tokens[1])
                self.ss = self.to_float(tokens[2])
            else:
                pass

        self.secs = (self.hh * 3600.0) + (self.mm * 60.0) + self.ss

    def to_float(self, s):
        try:
            return float(s)
        except ValueError:
            return float(0.0)

    def hours(self):
        return float(self.secs / Constants.seconds_per_hour())

    def as_hhmmss(self):
        hhs = self.zero_fill(self.hh)
        mms = self.zero_fill(self.mm)
        sss = self.zero_fill(self.ss)
        return "{0}:{1}:{2}".format(hhs, mms, sss)

    def zero_fill(self, n):
        if n < 10:
            return "0{0}".format(int(n))
        else:
            return "{0}".format(int(n))

    def __str__(self):
        template = "<ElapsedTime hh:{0} mm:{1} ss:{2} secs:{3}>"
        return template.format(self.hh, self.mm, self.ss, self.secs)

    def __repr__(self):
        return self.__str__()


class RunWalkCalculator(object):

    @classmethod
    def calculate(cls, run_hhmmss, run_ppm, walk_hhmmss, walk_ppm, miles):
        result = dict()
        result['run_hhmmss'] = run_hhmmss
        result['run_ppm'] = run_ppm
        result['walk_hhmmss'] = walk_hhmmss
        result['walk_ppm'] = walk_ppm
        result['miles'] = float(miles)

        if run_hhmmss and run_ppm and walk_hhmmss and walk_ppm and miles:
            run_duration_elapsed_time = ElapsedTime(run_hhmmss)
            run_ppm_elapsed_time = ElapsedTime(run_ppm)
            walk_duration_elapsed_time = ElapsedTime(walk_hhmmss)
            walk_ppm_elapsed_time = ElapsedTime(walk_ppm)
            distance = Distance(float(miles))
            mile = Distance(float(1.0))

            total_secs = float(run_duration_elapsed_time.secs +
                               walk_duration_elapsed_time.secs)
            run_pct = float(run_duration_elapsed_time.secs / total_secs)
            walk_pct = float(1.0 - run_pct)

            run_secs = float(run_pct * run_ppm_elapsed_time.secs)
            walk_secs = float(walk_pct * walk_ppm_elapsed_time.secs)
            avg_secs = float(run_secs + walk_secs)

            avg_time = ElapsedTime(avg_secs)
            avg_speed = Speed(mile, avg_time)

            result['avg_mph'] = avg_speed.mph()
            result['avg_ppm'] = avg_speed.pace_per_mile()
            result['proj_time'] = avg_speed.projected_time(distance)
            result['proj_miles'] = distance.as_miles()

        return result


class Speed(object):

    def __init__(self, d, et):
        self.dist = d    # an instance of Distance
        self.etime = et  # an instance of ElapsedTime

    def mph(self):
        return self.dist.as_miles() / self.etime.hours()

    def kph(self):
        return self.dist.as_kilometers() / self.etime.hours()

    def yph(self):
        return self.dist.as_yards() / self.etime.hours()

    def pace_per_mile(self):
        spm = self.seconds_per_mile()
        mm = math.floor(spm / 60.0)
        ss = spm - (mm * 60.0)

        if ss < 10:
            ss = "0{0}".format(ss)
        else:
            ss = "{0}".format(ss)

        if len(ss) > 5:
            ss = ss[0:5]

        return "{0}:{1}".format(mm, ss)

    def seconds_per_mile(self):
        return float(self.etime.secs / self.dist.as_miles())

    def projected_time(self, another_distance, algorithm='simple'):
        if algorithm is 'riegel':
            t1 = float(self.etime.secs)
            d1 = self.dist.as_miles()
            d2 = another_distance.as_miles()
            t2 = t1 * math.pow(float(d2 / d1), float(1.06))
            et = ElapsedTime(t2)
            return et.as_hhmmss()
        else:
            secs = float(self.seconds_per_mile() * another_distance.as_miles())
            et = ElapsedTime(secs)
            return et.as_hhmmss()

    def age_graded(self, event_age, graded_age):
        ag_factor = event_age.max_pulse() / graded_age.max_pulse()
        graded_secs = float((self.etime.secs)) * float(ag_factor)
        graded_et = ElapsedTime(graded_secs)
        return Speed(self.dist, graded_et)

    def __str__(self):
        template = "<Speed dist:{0} etime:{1}>"
        return template.format(self.dist, self.etime)

    def __repr__(self):
        return self.__str__()


# built on 2015-10-31 15:04:18.352176
