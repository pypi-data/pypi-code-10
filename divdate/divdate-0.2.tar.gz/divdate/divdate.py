import datetime


# Resolution levels
RES_NOTHING = 'N'
RES_YEAR = 'Y'
RES_MONTH = 'M'
RES_DAY = 'D'
RES_HOUR = 'h'
RES_MINUTE = 'm'
RES_SECOND = 's'
RES_MICROSECOND = 'ms'


class DivDate(datetime.date):
    def __new__(cls, year=1, month=1, day=1, resolution=RES_NOTHING):
        return super(DivDate, cls).__new__(cls, year, month, day)

    def __init__(self, year=1, month=1, day=1, resolution=RES_NOTHING):
        super(DivDate, self).__init__(year, month, day)
        self._resolution = resolution

    def __div__(self, field):
        if self._resolution == RES_NOTHING:
            return DivDate(field, resolution=RES_YEAR)
        elif self._resolution == RES_YEAR:
            return DivDate(self.year, field, resolution=RES_MONTH)
        elif self._resolution == RES_MONTH:
            return DivDate(self.year, self.month, field, resolution=RES_DAY)
        elif self._resolution == RES_DAY:
            return DivDateTime(self.year, self.month, self.day, field, resolution=RES_HOUR)
        else:
            raise ValueError('Invalid resolution')


class DivDateTime(datetime.datetime):
    def __new__(cls, year=1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None,
                resolution=RES_HOUR):
        return super(DivDateTime, cls).__new__(cls, year, month, day, hour, minute, second, microsecond, tzinfo)

    def __init__(self, year=1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None,
                 resolution=RES_HOUR):
        super(DivDateTime, self).__init__(year, month, day, hour, minute, second, microsecond, tzinfo)
        self._resolution = resolution

    def __div__(self, field):
        if self._resolution == RES_HOUR:
            return DivDateTime(self.year, self.month, self.day, self.hour, field, resolution=RES_MINUTE)
        elif self._resolution == RES_MINUTE:
            return DivDateTime(self.year, self.month, self.day, self.hour, self.minute, field, resolution=RES_SECOND)
        elif self._resolution == RES_SECOND:
            return DivDateTime(self.year, self.month, self.day, self.hour, self.minute, self.second, field,
                               resolution=RES_MICROSECOND)
        else:
            raise ValueError('End of resolution')
